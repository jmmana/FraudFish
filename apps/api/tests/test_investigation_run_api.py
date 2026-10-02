from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_demo_investigation_runs_registered_agents() -> None:
    case_response = client.post(
        "/cases",
        json={
            "case_ref": "FR-DEMO-ORCHESTRATOR",
            "title": "Demo orchestrator",
            "transaction_ids": [],
        },
    )
    case_id = case_response.json()["id"]

    start_response = client.post(f"/investigations/cases/{case_id}/start")
    investigation_id = start_response.json()["investigation_id"]

    run_response = client.post(f"/investigations/{investigation_id}/run")

    assert run_response.status_code == 200
    payload = run_response.json()
    assert payload["status"] == "succeeded"
    assert [agent["agent"] for agent in payload["agents"]] == ["ofac", "kyc"]
