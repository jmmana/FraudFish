from uuid import uuid4

from app.agents.contracts import AgentContext
from app.agents.source_verification import SourceVerificationAgent


def test_source_verification_flags_low_reliability_evidence() -> None:
    context = AgentContext(
        case_id=uuid4(),
        investigation_id=uuid4(),
        trace_id=uuid4(),
        inputs={
            "_prior_agent_results": [
                {
                    "agent": "osint_identity",
                    "evidence": [
                        {
                            "source_type": "social",
                            "source_ref": "fixture://social/1",
                            "reliability": "low",
                        },
                        {
                            "source_type": "news",
                            "source_ref": "fixture://news/1",
                            "reliability": "high",
                        },
                    ],
                }
            ]
        },
    )

    result = SourceVerificationAgent().run(context)

    assert result.metadata["reviewed_count"] == 2
    assert result.metadata["low_reliability_count"] == 1
    assert len(result.signals) == 1
