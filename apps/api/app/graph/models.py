from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class GraphNodeType(StrEnum):
    CASE = "case"
    PERSON = "person"
    ORGANIZATION = "organization"
    ACCOUNT = "account"
    TRANSACTION = "transaction"
    DEVICE = "device"
    IP = "ip"
    BENEFICIARY = "beneficiary"
    SOURCE = "source"
    EVIDENCE = "evidence"
    FINDING = "finding"


class GraphEdgeType(StrEnum):
    OWNS = "owns"
    USED = "used"
    OBSERVED_FROM = "observed_from"
    SENT = "sent"
    TO = "to"
    RESOLVES_TO = "resolves_to"
    SUPPORTS = "supports"
    ABOUT = "about"
    CONTAINS = "contains"
    RELATED_TO = "related_to"


class GraphNode(BaseModel):
    id: str
    type: GraphNodeType
    label: str
    properties: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    type: GraphEdgeType
    label: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)


class InvestigationGraph(BaseModel):
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)
