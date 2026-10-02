import os

from app.agents.adverse_media import AdverseMediaAgent
from app.agents.aml import TransactionAmlAgent
from app.agents.demo import DemoKycAgent
from app.agents.device import DeviceAgent
from app.agents.investigator import InvestigatorAgent
from app.agents.ofac import OfacAgent
from app.agents.osint import OsintIdentityAgent
from app.connectors.news import DemoNewsConnector, GdeltNewsConnector
from app.connectors.ofac import DemoOfacConnector, OfficialOfacConnector
from app.services.orchestrator import InvestigationOrchestrator


def build_ofac_agent() -> OfacAgent:
    source = os.getenv("FRAUDFISH_OFAC_SOURCE", "demo").strip().lower()
    connector = OfficialOfacConnector() if source == "official" else DemoOfacConnector()
    return OfacAgent(connector=connector)


def build_adverse_media_agent() -> AdverseMediaAgent:
    source = os.getenv("FRAUDFISH_NEWS_SOURCE", "demo").strip().lower()
    connector = GdeltNewsConnector() if source == "gdelt" else DemoNewsConnector()
    return AdverseMediaAgent(connector=connector)


def build_orchestrator() -> InvestigationOrchestrator:
    orchestrator = InvestigationOrchestrator()
    orchestrator.register(build_ofac_agent())
    orchestrator.register(DemoKycAgent())
    orchestrator.register(TransactionAmlAgent())
    orchestrator.register(DeviceAgent())
    orchestrator.register(OsintIdentityAgent())
    orchestrator.register(build_adverse_media_agent())
    orchestrator.register(InvestigatorAgent())
    return orchestrator


orchestrator = build_orchestrator()
