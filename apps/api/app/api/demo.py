from fastapi import APIRouter

from app.demo.scenario import build_demo_investigation_input
from app.domain.models import Case, Investigation, InvestigationStatus
from app.services.case_store import case_store
from app.services.runtime import orchestrator


router = APIRouter(prefix="/demo", tags=["demo"])


@router.post("/run")
def run_demo() -> dict:
    case = Case(
        case_ref="FR-2026-1042",
        title="Fictional suspicious transfer demo",
    )
    case_store.cases[case.id] = case

    investigation = Investigation(
        case_id=case.id,
        status=InvestigationStatus.QUEUED,
    )
    case_store.add_investigation(investigation)

    run = orchestrator.execute(
        investigation.id,
        inputs=build_demo_investigation_input(),
    )

    return {
        "case": case.model_dump(mode="json"),
        "investigation": {
            "id": str(investigation.id),
            "trace_id": str(investigation.trace_id),
            "status": run.status,
        },
        "agents": [result.model_dump(mode="json") for result in run.agent_results],
        "human_review_required": True,
    }
