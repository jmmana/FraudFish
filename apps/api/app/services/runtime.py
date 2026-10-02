from app.agents.aml import TransactionAmlAgent
from app.agents.demo import DemoKycAgent
from app.agents.ofac import OfacAgent
from app.agents.osint import OsintIdentityAgent
from app.services.orchestrator import InvestigationOrchestrator


def build_orchestrator() -> InvestigationOrchestrator:
    orchestrator = InvestigationOrchestrator()
    orchestrator.register(OfacAgent())
    orchestrator.register(DemoKycAgent())
    orchestrator.register(TransactionAmlAgent())
    orchestrator.register(OsintIdentityAgent())
    return orchestrator


orchestrator = build_orchestrator()
