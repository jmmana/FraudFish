from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PublicProfileRecord:
    source_type: str
    source_ref: str
    full_name: str
    country: str | None = None
    city: str | None = None
    occupation: str | None = None
    organization: str | None = None
    summary: str | None = None
    reliability: str = "medium"


class DemoOsintConnector:
    """Fictional public-source records for identity-resolution testing."""

    def __init__(self) -> None:
        self.records = (
            PublicProfileRecord(
                source_type="web",
                source_ref="fixture://osint/profile-001",
                full_name="Alejandro Torres Vega",
                country="CO",
                city="Medellin",
                occupation="Software Architect",
                organization="Demo Technology SAS",
                summary="Public professional profile in technology.",
                reliability="medium",
            ),
            PublicProfileRecord(
                source_type="news",
                source_ref="fixture://osint/news-001",
                full_name="Alejandro Torres Vega",
                country="MX",
                city="Monterrey",
                occupation="Business Owner",
                organization="Demo Imports SA",
                summary="Unrelated namesake mentioned in a fictional local business article.",
                reliability="high",
            ),
            PublicProfileRecord(
                source_type="social",
                source_ref="fixture://osint/social-001",
                full_name="Alejandro T. Vega",
                country="CO",
                city="Bogota",
                occupation="Content Creator",
                organization=None,
                summary="Public social profile; identity not established.",
                reliability="low",
            ),
        )

    def search_name(self, query: str) -> tuple[PublicProfileRecord, ...]:
        query_tokens = {token for token in query.lower().split() if token}
        return tuple(
            record
            for record in self.records
            if query_tokens.intersection(record.full_name.lower().split())
        )
