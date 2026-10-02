from app.connectors.osint import PublicProfileRecord
from app.services.identity_resolution import IdentityResolutionInput, resolve_candidate


def test_identity_resolution_rewards_contextual_matches() -> None:
    subject = IdentityResolutionInput(
        full_name="Alejandro Torres Vega",
        country="CO",
        city="Medellin",
        occupation="Software Architect",
    )
    record = PublicProfileRecord(
        source_type="web",
        source_ref="fixture://match",
        full_name="Alejandro Torres Vega",
        country="CO",
        city="Medellin",
        occupation="Software Architect",
    )

    result = resolve_candidate(subject, record)

    assert result.confidence >= 0.95
    assert "country" in result.matched_fields
    assert not result.conflicting_fields


def test_identity_resolution_penalizes_namesake_context_conflicts() -> None:
    subject = IdentityResolutionInput(
        full_name="Alejandro Torres Vega",
        country="CO",
        city="Medellin",
        occupation="Software Architect",
    )
    record = PublicProfileRecord(
        source_type="news",
        source_ref="fixture://namesake",
        full_name="Alejandro Torres Vega",
        country="MX",
        city="Monterrey",
        occupation="Business Owner",
    )

    result = resolve_candidate(subject, record)

    assert result.confidence < 0.60
    assert set(result.conflicting_fields) >= {"country", "city", "occupation"}
