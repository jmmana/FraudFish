from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from typing import Protocol

import httpx


@dataclass(frozen=True)
class SanctionsRecord:
    uid: str
    full_name: str
    aliases: tuple[str, ...] = ()
    date_of_birth: str | None = None
    nationality: str | None = None
    source_ref: str = "fixture://ofac/demo"


class OfacConnector(Protocol):
    def list_records(self) -> tuple[SanctionsRecord, ...]:
        ...


class DemoOfacConnector:
    """Fictional sanctions source for deterministic MVP testing."""

    def __init__(self) -> None:
        self.records = (
            SanctionsRecord(
                uid="OFAC-DEMO-001",
                full_name="Carlos Alberto Mendoza",
                aliases=("Carlos A. Mendoza",),
                date_of_birth="1978-04-11",
                nationality="VE",
            ),
            SanctionsRecord(
                uid="OFAC-DEMO-002",
                full_name="Global Meridian Trading LLC",
                aliases=("GMT LLC",),
                nationality="PA",
            ),
        )

    def list_records(self) -> tuple[SanctionsRecord, ...]:
        return self.records


class OfficialOfacConnector:
    """Downloads the official OFAC SDN legacy CSV series.

    The primary SDN file is joined to ALT.CSV using ENT_NUM so that
    alternate names participate in screening. Network access is isolated
    in the connector; matching remains deterministic in the agent.
    """

    DEFAULT_SDN_URL = (
        "https://sanctionslistservice.ofac.treas.gov/"
        "api/PublicationPreview/exports/sdn.csv"
    )
    DEFAULT_ALT_URL = (
        "https://sanctionslistservice.ofac.treas.gov/"
        "api/PublicationPreview/exports/alt.csv"
    )

    def __init__(
        self,
        sdn_url: str = DEFAULT_SDN_URL,
        alt_url: str = DEFAULT_ALT_URL,
        timeout_seconds: float = 20.0,
        user_agent: str = "FraudFish/0.1 sanctions-screening",
    ) -> None:
        self.sdn_url = sdn_url
        self.alt_url = alt_url
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent
        self._cache: tuple[SanctionsRecord, ...] | None = None

    def _download(self, url: str) -> str:
        response = httpx.get(
            url,
            timeout=self.timeout_seconds,
            follow_redirects=True,
            headers={"User-Agent": self.user_agent},
        )
        response.raise_for_status()
        return response.text

    @staticmethod
    def _parse_primary(text: str) -> dict[str, SanctionsRecord]:
        records: dict[str, SanctionsRecord] = {}
        reader = csv.reader(io.StringIO(text))

        for row in reader:
            if len(row) < 2:
                continue

            uid = row[0].strip()
            full_name = row[1].strip()
            if not uid or not full_name:
                continue

            records[uid] = SanctionsRecord(
                uid=uid,
                full_name=full_name,
                source_ref=OfficialOfacConnector.DEFAULT_SDN_URL,
            )

        return records

    @staticmethod
    def _parse_aliases(text: str) -> dict[str, list[str]]:
        aliases: dict[str, list[str]] = {}
        reader = csv.reader(io.StringIO(text))

        for row in reader:
            # Legacy ALT.CSV: ENT_NUM, ALT_NUM, ALT_TYPE, ALT_NAME, ...
            if len(row) < 4:
                continue

            uid = row[0].strip()
            alias_name = row[3].strip()
            if not uid or not alias_name:
                continue

            aliases.setdefault(uid, []).append(alias_name)

        return aliases

    def list_records(self) -> tuple[SanctionsRecord, ...]:
        if self._cache is not None:
            return self._cache

        primary = self._parse_primary(self._download(self.sdn_url))
        aliases = self._parse_aliases(self._download(self.alt_url))

        joined = []
        for uid, record in primary.items():
            joined.append(
                SanctionsRecord(
                    uid=record.uid,
                    full_name=record.full_name,
                    aliases=tuple(aliases.get(uid, [])),
                    source_ref=self.sdn_url,
                )
            )

        self._cache = tuple(joined)
        return self._cache
