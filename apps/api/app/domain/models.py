from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CaseStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    PENDING_HUMAN_REVIEW = "pending_human_review"
    CLOSED = "closed"


class InvestigationStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    PARTIAL = "partial"


class DecisionType(StrEnum):
    CLOSE = "close"
    ESCALATE = "escalate"
    REQUEST_EDD = "request_edd"
    REQUEST_SOURCE_OF_FUNDS = "request_source_of_funds"
    REQUEST_SOURCE_OF_WEALTH = "request_source_of_wealth"
    OTHER = "other"


class SourceType(StrEnum):
    INTERNAL = "internal"
    SANCTIONS = "sanctions"
    PUBLIC_RECORD = "public_record"
    NEWS = "news"
    SOCIAL = "social"
    WEB = "web"
    DEVICE = "device"
    TRANSACTION = "transaction"


class Reliability(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    AUTHORITATIVE = "authoritative"


class SignalSeverity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class HypothesisState(StrEnum):
    OPEN = "open"
    SUPPORTED = "supported"
    WEAKENED = "weakened"
    REJECTED = "rejected"


class Person(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    full_name: str
    document_id: str | None = None
    date_of_birth: str | None = None
    nationality: str | None = None
    country_of_residence: str | None = None
    occupation: str | None = None


class Organization(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    legal_name: str
    registration_id: str | None = None
    country: str | None = None
    industry: str | None = None


class Account(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    owner_person_id: UUID | None = None
    owner_organization_id: UUID | None = None
    institution: str
    account_ref: str
    currency: str


class Device(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    device_ref: str
    fingerprint: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None


class Transaction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    external_ref: str
    sender_person_id: UUID | None = None
    sender_account_id: UUID | None = None
    beneficiary_person_id: UUID | None = None
    beneficiary_account_id: UUID | None = None
    device_id: UUID | None = None
    amount: float = Field(gt=0)
    currency: str
    occurred_at: datetime
    channel: str | None = None
    origin_city: str | None = None
    destination_city: str | None = None


class Case(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    case_ref: str
    title: str
    status: CaseStatus = CaseStatus.OPEN
    subject_person_id: UUID | None = None
    subject_organization_id: UUID | None = None
    transaction_ids: list[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Investigation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    case_id: UUID
    status: InvestigationStatus = InvestigationStatus.QUEUED
    trace_id: UUID = Field(default_factory=uuid4)
    started_at: datetime | None = None
    completed_at: datetime | None = None


class Signal(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    case_id: UUID
    source_type: SourceType
    signal_type: str
    summary: str
    severity: SignalSeverity = SignalSeverity.INFO
    observed_at: datetime = Field(default_factory=utc_now)
    source_ref: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class Evidence(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    case_id: UUID
    source_type: SourceType
    source_ref: str
    collected_at: datetime = Field(default_factory=utc_now)
    reliability: Reliability
    payload: dict[str, Any]
    corroborated: bool = False
    content_hash: str | None = None


class Finding(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    case_id: UUID
    agent: str
    statement: str
    evidence_ids: list[UUID] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    created_at: datetime = Field(default_factory=utc_now)


class Hypothesis(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    case_id: UUID
    statement: str
    state: HypothesisState = HypothesisState.OPEN
    supporting_finding_ids: list[UUID] = Field(default_factory=list)
    contradicting_finding_ids: list[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class IdentityCandidate(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    case_id: UUID
    candidate_ref: str
    source_refs: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    matched_fields: list[str] = Field(default_factory=list)
    conflicting_fields: list[str] = Field(default_factory=list)
    analyst_confirmed: bool | None = None


class HumanDecision(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    case_id: UUID
    investigation_id: UUID | None = None
    decision: DecisionType
    rationale: str
    analyst: str
    created_at: datetime = Field(default_factory=utc_now)
