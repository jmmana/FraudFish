from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.models import CaseStatus, DecisionType, InvestigationStatus


class CaseCreate(BaseModel):
    case_ref: str = Field(min_length=1, max_length=128)
    title: str = Field(min_length=1, max_length=255)
    subject_person_id: UUID | None = None
    subject_organization_id: UUID | None = None
    transaction_ids: list[UUID] = Field(default_factory=list)


class CaseSummary(BaseModel):
    id: UUID
    case_ref: str
    title: str
    status: CaseStatus
    created_at: datetime
    updated_at: datetime


class InvestigationStartResponse(BaseModel):
    investigation_id: UUID
    case_id: UUID
    trace_id: UUID
    status: InvestigationStatus


class HumanDecisionCreate(BaseModel):
    investigation_id: UUID | None = None
    decision: DecisionType
    rationale: str = Field(min_length=3, max_length=4000)
    analyst: str = Field(min_length=1, max_length=255)
