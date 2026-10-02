from __future__ import annotations

from enum import StrEnum
from typing import Any, Protocol
from uuid import UUID

from pydantic import BaseModel, Field


class AgentStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class AgentContext(BaseModel):
    case_id: UUID
    investigation_id: UUID
    trace_id: UUID
    inputs: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    agent: str
    status: AgentStatus
    summary: str
    signals: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    findings: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class InvestigationAgent(Protocol):
    name: str

    def run(self, context: AgentContext) -> AgentResult:
        ...
