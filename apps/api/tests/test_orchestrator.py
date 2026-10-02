from uuid import uuid4

import pytest

from app.agents.contracts import AgentContext, AgentResult, AgentStatus
from app.domain.models import Case, Investigation
from app.services.case_store import case_store
from app.services.orchestrator import InvestigationOrchestrator


class SuccessAgent:
    name = "success"

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent=self.name,
            status=AgentStatus.SUCCEEDED,
            summary="ok",
        )


class BrokenAgent:
    name = "broken"

    def run(self, context: AgentContext) -> AgentResult:
        raise RuntimeError("fixture failure")


def test_orchestrator_returns_partial_when_one_agent_fails() -> None:
    case = Case(case_ref=f"CASE-{uuid4()}", title="Orchestrator test")
    case_store.cases[case.id] = case

    investigation = Investigation(case_id=case.id)
    case_store.investigations[investigation.id] = investigation

    orchestrator = InvestigationOrchestrator()
    orchestrator.register(SuccessAgent())
    orchestrator.register(BrokenAgent())

    run = orchestrator.execute(investigation.id)

    assert run.status == "partial"
    assert run.agent_results[0].status == "succeeded"
    assert run.agent_results[1].status == "failed"
    assert run.agent_results[1].error == "fixture failure"


def test_duplicate_agent_registration_is_rejected() -> None:
    orchestrator = InvestigationOrchestrator()
    orchestrator.register(SuccessAgent())

    with pytest.raises(ValueError):
        orchestrator.register(SuccessAgent())
