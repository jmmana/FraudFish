from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_case_lifecycle() -> None:
    create_response = client.post(
        "/cases",
        json={
            "case_ref": "FR-2026-1042",
            "title": "Suspicious transfer demo",
            "transaction_ids": [],
        },
    )
    assert create_response.status_code == 201

    case = create_response.json()
    case_id = case["id"]

    get_response = client.get(f"/cases/{case_id}")
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "open"

    start_response = client.post(f"/investigations/cases/{case_id}/start")
    assert start_response.status_code == 202
    assert start_response.json()["status"] == "running"

    decision_response = client.post(
        f"/cases/{case_id}/decisions",
        json={
            "investigation_id": start_response.json()["investigation_id"],
            "decision": "escalate",
            "rationale": "Multiple corroborated signals require analyst escalation.",
            "analyst": "demo-analyst",
        },
    )
    assert decision_response.status_code == 200
    assert decision_response.json()["decision"] == "escalate"
