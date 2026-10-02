from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SanctionsRecord:
    uid: str
    full_name: str
    aliases: tuple[str, ...] = ()
    date_of_birth: str | None = None
    nationality: str | None = None
    source_ref: str = "fixture://ofac/demo"


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
