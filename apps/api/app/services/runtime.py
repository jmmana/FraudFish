from app.agents.demo import DemoKycAgent
from app.agents.ofac import OfacAgent
from app.services.orchestrator import InvestigationOrchestrator


def build_orchestrator() -> InvestigationOrchestrator:
    orchestrator = InvestigationOrchestrator()
    orchestrator.register(OfacAgent())
    orchestrator.register(DemoKycAgent())
    return orchestrator


orchestrator = build_orchestrator()
