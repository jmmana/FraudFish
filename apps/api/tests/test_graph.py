from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_demo_graph_contains_expected_network_patterns() -> None:
    response = client.get("/graph/demo")

    assert response.status_code == 200
    payload = response.json()

    nodes = payload["nodes"]
    edges = payload["edges"]

    device = next(node for node in nodes if node["id"] == "device:8732")
    beneficiary = next(node for node in nodes if node["id"] == "beneficiary:4421")

    assert device["properties"]["linked_identity_count"] == 6
    assert beneficiary["properties"]["sender_count"] == 14

    device_edges = [
        edge for edge in edges
        if edge["target"] == "device:8732" and edge["type"] == "used"
    ]
    beneficiary_edges = [
        edge for edge in edges
        if edge["target"] == "beneficiary:4421" and edge["type"] == "to"
    ]

    assert len(device_edges) == 7
    assert len(beneficiary_edges) == 14
