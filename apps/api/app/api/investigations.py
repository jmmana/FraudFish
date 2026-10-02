from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.domain.models import Investigation, InvestigationStatus
from app.domain.schemas import InvestigationStartResponse
from app.services.case_store import case_store


router = APIRouter(prefix="/investigations", tags=["investigations"])


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
