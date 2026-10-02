from uuid import uuid4

from app.agents.contracts import AgentContext
from app.agents.investigator import InvestigatorAgent


def test_investigator_prioritizes_high_risk_without_making_human_decision() -> None:
    context = AgentContext(
        case_id=uuid4(),
        investigation_id=uuid4(),
        trace_id=uuid4(),
        inputs={
            "_prior_agent_results": [
                {
                    "agent": "aml",
                    "status": "succeeded",
                    "signals": [
                        {"severity": "high"},
                        {"severity": "high"},
                        {"severity": "medium"},
                    ],
                },
                {
                    "agent": "device",
                    "status": "succeeded",
                    "signals": [{"severity": "high"}],
                },
            ]
        },
    )

    result = InvestigatorAgent().run(context)

    assert result.metadata["risk_band"] == "high"
    assert result.metadata["human_decision_required"] is True
    assert result.metadata["autonomous_enforcement_allowed"] is False
