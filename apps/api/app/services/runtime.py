from app.agents.aml import TransactionAmlAgent
from app.agents.demo import DemoKycAgent
from app.agents.device import DeviceAgent
from app.agents.investigator import InvestigatorAgent
from app.agents.ofac import OfacAgent
from app.agents.osint import OsintIdentityAgent
from app.services.orchestrator import InvestigationOrchestrator


def build_orchestrator() -> InvestigationOrchestrator:
    orchestrator = InvestigationOrchestrator()
    orchestrator.register(OfacAgent())
    orchestrator.register(DemoKycAgent())
    orchestrator.register(TransactionAmlAgent())
    orchestrator.register(DeviceAgent())
    orchestrator.register(OsintIdentityAgent())
    orchestrator.register(InvestigatorAgent())
    return orchestrator


orchestrator = build_orchestrator()
