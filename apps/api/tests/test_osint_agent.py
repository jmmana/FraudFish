from uuid import uuid4

from app.agents.contracts import AgentContext
from app.agents.osint import OsintIdentityAgent


def test_osint_agent_returns_candidates_without_confirming_identity() -> None:
    context = AgentContext(
        case_id=uuid4(),
        investigation_id=uuid4(),
        trace_id=uuid4(),
        inputs={
            "subject_name": "Alejandro Torres Vega",
            "subject_country": "CO",
            "subject_city": "Medellin",
            "subject_occupation": "Software Architect",
        },
    )

    result = OsintIdentityAgent().run(context)

    assert result.status == "succeeded"
    assert result.metadata["candidate_count"] >= 2
    assert result.metadata["identity_confirmed"] is False
    assert result.metadata["human_validation_required"] is True
    assert any(
        evidence["source_type"] == "social"
        for evidence in result.evidence
    )
