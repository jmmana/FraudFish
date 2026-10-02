from __future__ import annotations

import os

from app.graph.demo_builder import build_demo_graph
from app.graph.repository import Neo4jGraphRepository


def main() -> None:
    repository = Neo4jGraphRepository(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD", "change-me-now"),
    )
    try:
        repository.verify_connectivity()
        repository.upsert_graph(build_demo_graph())
        print("FraudFish demo graph seeded successfully.")
    finally:
        repository.close()


if __name__ == "__main__":
    main()
