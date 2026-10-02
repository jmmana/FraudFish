from uuid import uuid4

from app.agents.contracts import AgentContext
from app.agents.ofac import OfacAgent
from app.services.name_matching import normalize_name


def context(subject_name: str) -> AgentContext:
    return AgentContext(
        case_id=uuid4(),
        investigation_id=uuid4(),
        trace_id=uuid4(),
        inputs={"subject_name": subject_name},
    )


def test_name_normalization_removes_accents_and_punctuation() -> None:
    assert normalize_name("  José-Pérez  ") == "jose perez"


def test_ofac_agent_returns_no_match_for_unrelated_name() -> None:
    result = OfacAgent().run(context("Alejandro Torres Vega"))

    assert result.status == "succeeded"
    assert result.metadata["positive_match_count"] == 0


def test_ofac_agent_flags_exact_fixture_candidate_without_confirming_identity() -> None:
    result = OfacAgent().run(context("Carlos Alberto Mendoza"))

    assert result.status == "succeeded"
    assert result.metadata["positive_match_count"] == 1
    assert "identity is not confirmed" in result.findings[0]["statement"].lower()
