from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.domain.models import Investigation, InvestigationStatus
from app.domain.schemas import InvestigationStartResponse
from app.services.case_store import case_store
from app.services.runtime import orchestrator


router = APIRouter(prefix="/investigations", tags=["investigations"])


class InvestigationRunRequest(BaseModel):
    subject_name: str | None = Field(default=None, max_length=255)
    subject_country: str | None = Field(default=None, max_length=64)
    subject_city: str | None = Field(default=None, max_length=128)
    subject_occupation: str | None = Field(default=None, max_length=255)
    subject_organization: str | None = Field(default=None, max_length=255)
    transactions: list[dict[str, Any]] = Field(default_factory=list)
    device_links: list[dict[str, Any]] = Field(default_factory=list)


@router.post(
    "/cases/{case_id}/start",
    response_model=InvestigationStartResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def start_investigation(case_id: UUID) -> InvestigationStartResponse:
    case = case_store.get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    investigation = Investigation(
        case_id=case_id,
        status=InvestigationStatus.RUNNING,
        started_at=datetime.now(timezone.utc),
    )
    case_store.add_investigation(investigation)

    return InvestigationStartResponse(
        investigation_id=investigation.id,
        case_id=case_id,
        trace_id=investigation.trace_id,
        status=investigation.status,
    )


@router.post("/{investigation_id}/run")
def run_investigation(
    investigation_id: UUID,
    payload: InvestigationRunRequest | None = None,
) -> dict:
    investigation = case_store.investigations.get(investigation_id)
    if investigation is None:
        raise HTTPException(status_code=404, detail="Investigation not found")

    inputs = payload.model_dump(exclude_none=True) if payload else {}
    run = orchestrator.execute(investigation_id, inputs=inputs)

    return {
        "investigation_id": str(run.investigation_id),
        "trace_id": str(run.trace_id),
        "status": run.status,
        "agents": [result.model_dump(mode="json") for result in run.agent_results],
    }


@router.get("/{investigation_id}/agents")
def list_investigation_agents(investigation_id: UUID) -> dict:
    if investigation_id not in case_store.investigations:
        raise HTTPException(status_code=404, detail="Investigation not found")

    return {"agents": orchestrator.registered_agents()}
