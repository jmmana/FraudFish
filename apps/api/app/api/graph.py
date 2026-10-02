from fastapi import APIRouter

from app.graph.demo_builder import build_demo_graph
from app.graph.models import InvestigationGraph


router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/demo", response_model=InvestigationGraph)
def get_demo_graph() -> InvestigationGraph:
    return build_demo_graph()
