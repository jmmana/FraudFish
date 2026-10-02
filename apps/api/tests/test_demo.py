from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_demo_runs_end_to_end() -> None:
    response = client.post("/demo/run")

    assert response.status_code == 200
    payload = response.json()

    assert payload["case"]["case_ref"] == "FR-2026-1042"
    assert payload["investigation"]["status"] == "succeeded"
    assert payload["human_review_required"] is True

    agent_names = [agent["agent"] for agent in payload["agents"]]
    assert agent_names == ["ofac", "kyc", "aml", "osint_identity"]

    aml = next(agent for agent in payload["agents"] if agent["agent"] == "aml")
    aml_signal_types = {signal["signal_type"] for signal in aml["signals"]}
    assert "high_velocity" in aml_signal_types
    assert "common_beneficiary" in aml_signal_types

    osint = next(agent for agent in payload["agents"] if agent["agent"] == "osint_identity")
    assert osint["metadata"]["human_validation_required"] is True
