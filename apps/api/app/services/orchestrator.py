from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
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
    def __init__(
        self,
        agent_timeout_seconds: float = 15.0,
        max_attempts: int = 2,
    ) -> None:
        if agent_timeout_seconds <= 0:
            raise ValueError("agent_timeout_seconds must be positive")
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        self._agents: list[InvestigationAgent] = []
        self.agent_timeout_seconds = agent_timeout_seconds
        self.max_attempts = max_attempts

    def register(self, agent: InvestigationAgent) -> None:
        if any(existing.name == agent.name for existing in self._agents):
            raise ValueError(f"Agent already registered: {agent.name}")
        self._agents.append(agent)

    def registered_agents(self) -> list[str]:
        return [agent.name for agent in self._agents]

    def _execute_agent(
        self,
        agent: InvestigationAgent,
        context: AgentContext,
    ) -> AgentResult:
        last_error: str | None = None

        for attempt in range(1, self.max_attempts + 1):
            executor = ThreadPoolExecutor(max_workers=1)
            future = executor.submit(agent.run, context)

            try:
                result = future.result(timeout=self.agent_timeout_seconds)
                executor.shutdown(wait=False, cancel_futures=True)
                result.metadata.setdefault("attempts", attempt)
                return result
            except FutureTimeoutError:
                last_error = (
                    f"Agent timed out after {self.agent_timeout_seconds} seconds "
                    f"on attempt {attempt}."
                )
                future.cancel()
                executor.shutdown(wait=False, cancel_futures=True)
            except Exception as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                executor.shutdown(wait=False, cancel_futures=True)

        return AgentResult(
            agent=agent.name,
            status=AgentStatus.FAILED,
            summary="Agent execution failed after bounded retries.",
            error=last_error,
            metadata={"attempts": self.max_attempts},
        )

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

            result = self._execute_agent(agent, context)
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
