from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AuditEventType(StrEnum):
    CASE_CREATED = "case_created"
    INVESTIGATION_STARTED = "investigation_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"
    HUMAN_DECISION_RECORDED = "human_decision_recorded"


class AuditEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    event_type: AuditEventType
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    trace_id: UUID | None = None
    case_id: UUID | None = None
    investigation_id: UUID | None = None
    actor: str = "system"
    metadata: dict[str, Any] = Field(default_factory=dict)


class InMemoryAuditStore:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def append(self, event: AuditEvent) -> None:
        self.events.append(event)

    def for_case(self, case_id: UUID) -> list[AuditEvent]:
        return [event for event in self.events if event.case_id == case_id]


audit_store = InMemoryAuditStore()
