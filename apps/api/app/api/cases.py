from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.domain.models import Case, HumanDecision
from app.domain.schemas import CaseCreate, CaseSummary, HumanDecisionCreate
from app.services.case_store import case_store


router = APIRouter(prefix="/cases", tags=["cases"])


@router.post("", response_model=CaseSummary, status_code=status.HTTP_201_CREATED)
def create_case(payload: CaseCreate) -> Case:
    return case_store.create_case(payload)


@router.get("/{case_id}", response_model=CaseSummary)
def get_case(case_id: UUID) -> Case:
    case = case_store.get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.post("/{case_id}/decisions", response_model=HumanDecision)
def create_human_decision(
    case_id: UUID,
    payload: HumanDecisionCreate,
) -> HumanDecision:
    if case_store.get_case(case_id) is None:
        raise HTTPException(status_code=404, detail="Case not found")

    return case_store.add_decision(case_id, payload)
