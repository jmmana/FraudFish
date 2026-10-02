from datetime import datetime, timedelta, timezone

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

    now = datetime.now(timezone.utc)
    transactions = [
        {
            "transaction_ref": f"TX-{index}",
            "amount": 9800000,
            "occurred_at": (now - timedelta(hours=index * 4)).isoformat(),
            "beneficiary_ref": "BEN-4421",
        }
        for index in range(8)
    ]

    run_response = client.post(
        f"/investigations/{investigation_id}/run",
        json={
            "subject_name": "Alejandro Torres Vega",
            "transactions": transactions,
        },
    )

    assert run_response.status_code == 200
    payload = run_response.json()
    assert payload["status"] == "succeeded"
    assert [agent["agent"] for agent in payload["agents"]] == ["ofac", "kyc", "aml"]
    assert payload["agents"][0]["metadata"]["positive_match_count"] == 0
    assert len(payload["agents"][2]["signals"]) >= 2
