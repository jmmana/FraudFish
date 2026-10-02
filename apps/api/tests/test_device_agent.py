from uuid import uuid4

from app.agents.contracts import AgentContext
from app.agents.device import DeviceAgent


def test_device_agent_detects_shared_device() -> None:
    links = [
        {"device_ref": "DEV-8732", "identity_ref": f"PERSON-{index}"}
        for index in range(1, 7)
    ]
    context = AgentContext(
        case_id=uuid4(),
        investigation_id=uuid4(),
        trace_id=uuid4(),
        inputs={"device_links": links},
    )

    result = DeviceAgent().run(context)

    assert result.status == "succeeded"
    assert len(result.signals) == 1
    assert "6 identities" in result.signals[0]["summary"]
