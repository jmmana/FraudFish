from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from app.agents.contracts import (
    AgentContext,
    AgentResult,
    AgentStatus,
    InvestigationAgent,
)
from app.domain.models import InvestigationStatus
from app.services.case_store import case_store


@dataclass
class InvestigationRun:
    investigation_id: UUID
    trace_id: UUID
    status: InvestigationStatus
    agent_results: list[AgentResult] = field(default_factory=list)


class InvestigationOrchestrator:
    def __init__(self) -> None:
        self._agents: list[InvestigationAgent] = []

    def register(self, agent: InvestigationAgent) -> None:
        if any(existing.name == agent.name for existing in self._agents):
            raise ValueError(f"Agent already registered: {agent.name}")
        self._agents.append(agent)

    def registered_agents(self) -> list[str]:
        return [agent.name for agent in self._agents]

    def execute(
        self,
        investigation_id: UUID,
        inputs: dict[str, Any] | None = None,
    ) -> InvestigationRun:
        investigation = case_store.investigations.get(investigation_id)
        if investigation is None:
            raise KeyError("Investigation not found")

        investigation.status = InvestigationStatus.RUNNING
        if investigation.started_at is None:
            investigation.started_at = datetime.now(timezone.utc)

        base_inputs = dict(inputs or {})
        results: list[AgentResult] = []
        failed = False

        for agent in self._agents:
            context_inputs = dict(base_inputs)
            context_inputs["_prior_agent_results"] = [
                result.model_dump(mode="json")
                for result in results
            ]
            context = AgentContext(
                case_id=investigation.case_id,
                investigation_id=investigation.id,
                trace_id=investigation.trace_id,
                inputs=context_inputs,
            )

            try:
                result = agent.run(context)
            except Exception as exc:
                failed = True
                result = AgentResult(
                    agent=agent.name,
                    status=AgentStatus.FAILED,
                    summary="Agent execution failed.",
                    error=str(exc),
                )

            if result.status == AgentStatus.FAILED:
                failed = True

            results.append(result)

        investigation.completed_at = datetime.now(timezone.utc)

        if failed and any(r.status == AgentStatus.SUCCEEDED for r in results):
            investigation.status = InvestigationStatus.PARTIAL
        elif failed:
            investigation.status = InvestigationStatus.FAILED
        else:
            investigation.status = InvestigationStatus.SUCCEEDED

        return InvestigationRun(
            investigation_id=investigation.id,
            trace_id=investigation.trace_id,
            status=investigation.status,
            agent_results=results,
        )
