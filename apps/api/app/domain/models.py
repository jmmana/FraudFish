from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SourceType(StrEnum):
    INTERNAL = "internal"
    SANCTIONS = "sanctions"
    PUBLIC_RECORD = "public_record"
    NEWS = "news"
    SOCIAL = "social"
    WEB = "web"


class Reliability(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    AUTHORITATIVE = "authoritative"


class Evidence(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    case_id: UUID
    source_type: SourceType
    source_ref: str
    collected_at: datetime
    reliability: Reliability
    payload: dict[str, Any]
    corroborated: bool = False


class Finding(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    case_id: UUID
    agent: str
    statement: str
    evidence_ids: list[UUID]
    confidence: float = Field(ge=0, le=1)


class IdentityCandidate(BaseModel):
    candidate_ref: str
    confidence: float = Field(ge=0, le=1)
    matched_fields: list[str] = []
    conflicting_fields: list[str] = []
    analyst_confirmed: bool | None = None
