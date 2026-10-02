from uuid import uuid4

from app.agents.adverse_media import AdverseMediaAgent
from app.agents.contracts import AgentContext
from app.connectors.news import NewsArticle


class FixtureNewsConnector:
    def search(self, full_name: str) -> tuple[NewsArticle, ...]:
        return (
            NewsArticle(
                title=f"{full_name} mentioned in fraud investigation",
                url="fixture://news/adverse-001",
                source_domain="fixture.example",
            ),
        )


def test_adverse_media_agent_creates_candidate_not_conclusion() -> None:
    context = AgentContext(
        case_id=uuid4(),
        investigation_id=uuid4(),
        trace_id=uuid4(),
        inputs={"subject_name": "Alejandro Torres Vega"},
    )

    result = AdverseMediaAgent(FixtureNewsConnector()).run(context)

    assert result.status == "succeeded"
    assert len(result.signals) == 1
    assert result.metadata["identity_confirmed"] is False
    assert result.metadata["human_validation_required"] is True
    assert "No article alone confirms identity or wrongdoing." in result.findings[0]["statement"]
