from app.agents.demo import DemoKycAgent, DemoOFACAgent
from app.services.orchestrator import InvestigationOrchestrator


def build_orchestrator() -> InvestigationOrchestrator:
    orchestrator = InvestigationOrchestrator()
    orchestrator.register(DemoOFACAgent())
    orchestrator.register(DemoKycAgent())
    return orchestrator


orchestrator = build_orchestrator()
