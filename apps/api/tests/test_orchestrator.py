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
    assert "fixture failure" in (run.agent_results[1].error or "")


def test_duplicate_agent_registration_is_rejected() -> None:
    orchestrator = InvestigationOrchestrator()
    orchestrator.register(SuccessAgent())

    with pytest.raises(ValueError):
        orchestrator.register(SuccessAgent())


class FlakyAgent:
    name = "flaky"

    def __init__(self) -> None:
        self.calls = 0

    def run(self, context: AgentContext) -> AgentResult:
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("temporary")
        return AgentResult(
            agent=self.name,
            status=AgentStatus.SUCCEEDED,
            summary="recovered",
        )


def test_orchestrator_retries_transient_failure() -> None:
    case = Case(case_ref=f"CASE-{uuid4()}", title="Retry test")
    case_store.cases[case.id] = case
    investigation = Investigation(case_id=case.id)
    case_store.investigations[investigation.id] = investigation

    agent = FlakyAgent()
    orchestrator = InvestigationOrchestrator(max_attempts=2)
    orchestrator.register(agent)

    run = orchestrator.execute(investigation.id)

    assert run.status == "succeeded"
    assert agent.calls == 2
    assert run.agent_results[0].metadata["attempts"] == 2
