from __future__ import annotations

from collections.abc import Iterable

from neo4j import Driver, GraphDatabase

from app.graph.models import GraphEdge, GraphNode, InvestigationGraph


class Neo4jGraphRepository:
    def __init__(self, uri: str, user: str, password: str) -> None:
        self._driver: Driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        self._driver.close()

    def verify_connectivity(self) -> None:
        self._driver.verify_connectivity()

    def upsert_graph(self, graph: InvestigationGraph) -> None:
        with self._driver.session() as session:
            for node in graph.nodes:
                session.execute_write(self._upsert_node, node)
            for edge in graph.edges:
                session.execute_write(self._upsert_edge, edge)

    @staticmethod
    def _upsert_node(tx, node: GraphNode) -> None:
        tx.run(
            """
            MERGE (n:FraudFishEntity {id: $id})
            SET n.type = $type,
                n.label = $label,
                n.properties = $properties
            """,
            id=node.id,
            type=node.type.value,
            label=node.label,
            properties=node.properties,
        )

    @staticmethod
    def _upsert_edge(tx, edge: GraphEdge) -> None:
        tx.run(
            """
            MATCH (source:FraudFishEntity {id: $source})
            MATCH (target:FraudFishEntity {id: $target})
            MERGE (source)-[r:RELATED {id: $id}]->(target)
            SET r.type = $type,
                r.label = $label,
                r.properties = $properties
            """,
            id=edge.id,
            source=edge.source,
            target=edge.target,
            type=edge.type.value,
            label=edge.label,
            properties=edge.properties,
        )

    def fetch_graph(self) -> InvestigationGraph:
        with self._driver.session() as session:
            node_records = session.run(
                """
                MATCH (n:FraudFishEntity)
                RETURN n.id AS id, n.type AS type, n.label AS label, n.properties AS properties
                """
            )
            nodes = [
                GraphNode(
                    id=record["id"],
                    type=record["type"],
                    label=record["label"],
                    properties=record["properties"] or {},
                )
                for record in node_records
            ]

            edge_records = session.run(
                """
                MATCH (source:FraudFishEntity)-[r:RELATED]->(target:FraudFishEntity)
                RETURN r.id AS id,
                       source.id AS source,
                       target.id AS target,
                       r.type AS type,
                       r.label AS label,
                       r.properties AS properties
                """
            )
            edges = [
                GraphEdge(
                    id=record["id"],
                    source=record["source"],
                    target=record["target"],
                    type=record["type"],
                    label=record["label"],
                    properties=record["properties"] or {},
                )
                for record in edge_records
            ]

        return InvestigationGraph(nodes=nodes, edges=edges)
