from __future__ import annotations

from app.graph.models import (
    GraphEdge,
    GraphEdgeType,
    GraphNode,
    GraphNodeType,
    InvestigationGraph,
)


def build_demo_graph() -> InvestigationGraph:
    nodes: list[GraphNode] = [
        GraphNode(id="case:FR-2026-1042", type=GraphNodeType.CASE, label="FR-2026-1042"),
        GraphNode(
            id="person:subject",
            type=GraphNodeType.PERSON,
            label="Juan Manuel Castillo Pinto",
            properties={"role": "subject", "identity_status": "known"},
        ),
        GraphNode(
            id="device:8732",
            type=GraphNodeType.DEVICE,
            label="DEV-8732",
            properties={"linked_identity_count": 6, "risk": "high"},
        ),
        GraphNode(
            id="ip:181-x-x-42",
            type=GraphNodeType.IP,
            label="181.x.x.42",
        ),
        GraphNode(
            id="beneficiary:4421",
            type=GraphNodeType.BENEFICIARY,
            label="Beneficiary 4421",
            properties={"sender_count": 14, "risk": "high"},
        ),
    ]

    edges: list[GraphEdge] = [
        GraphEdge(
            id="edge:case-subject",
            source="case:FR-2026-1042",
            target="person:subject",
            type=GraphEdgeType.CONTAINS,
        ),
        GraphEdge(
            id="edge:subject-device",
            source="person:subject",
            target="device:8732",
            type=GraphEdgeType.USED,
        ),
        GraphEdge(
            id="edge:device-ip",
            source="device:8732",
            target="ip:181-x-x-42",
            type=GraphEdgeType.OBSERVED_FROM,
        ),
    ]

    for index in range(1, 7):
        node_id = f"person:linked-{index}"
        nodes.append(
            GraphNode(
                id=node_id,
                type=GraphNodeType.PERSON,
                label=f"Linked Identity {index}",
                properties={"identity_status": "candidate"},
            )
        )
        edges.append(
            GraphEdge(
                id=f"edge:linked-{index}-device",
                source=node_id,
                target="device:8732",
                type=GraphEdgeType.USED,
                properties={"derived_from": "device_intelligence"},
            )
        )

    for index in range(1, 15):
        sender_id = f"person:sender-{index}"
        tx_id = f"transaction:{index:02d}"

        nodes.extend([
            GraphNode(
                id=sender_id,
                type=GraphNodeType.PERSON,
                label=f"Sender {index}",
                properties={"role": "sender"},
            ),
            GraphNode(
                id=tx_id,
                type=GraphNodeType.TRANSACTION,
                label=f"TX-{index:02d}",
                properties={
                    "amount": 9_800_000 if index <= 8 else 2_100_000 + index * 100_000,
                    "currency": "COP",
                },
            ),
        ])

        edges.extend([
            GraphEdge(
                id=f"edge:{sender_id}:{tx_id}",
                source=sender_id,
                target=tx_id,
                type=GraphEdgeType.SENT,
            ),
            GraphEdge(
                id=f"edge:{tx_id}:beneficiary",
                source=tx_id,
                target="beneficiary:4421",
                type=GraphEdgeType.TO,
            ),
        ])

    nodes.extend([
        GraphNode(
            id="source:web-profile",
            type=GraphNodeType.SOURCE,
            label="Public professional profile",
            properties={"reliability": "medium"},
        ),
        GraphNode(
            id="source:namesake-news",
            type=GraphNodeType.SOURCE,
            label="Namesake news result",
            properties={"reliability": "high", "identity_confidence": 0.40},
        ),
    ])

    edges.extend([
        GraphEdge(
            id="edge:profile-subject",
            source="source:web-profile",
            target="person:subject",
            type=GraphEdgeType.RELATED_TO,
            properties={"identity_confidence": 0.98, "human_validated": False},
        ),
        GraphEdge(
            id="edge:namesake-subject",
            source="source:namesake-news",
            target="person:subject",
            type=GraphEdgeType.RELATED_TO,
            properties={"identity_confidence": 0.40, "human_validated": False},
        ),
    ])

    return InvestigationGraph(nodes=nodes, edges=edges)
