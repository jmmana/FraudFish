# Architecture Overview

## Goal

FraudFish coordinates deterministic controls, specialized AI agents, graph analysis and OSINT to produce traceable investigation findings for a human analyst.

## High-level flow

```text
Case / Transaction
        |
        v
Investigation Orchestrator
        |
        +---------------------------+
        |                           |
        v                           v
Deterministic Controls        AI Investigation Agents
OFAC / rules / KYC checks     OSINT / identity / context
        |                           |
        +-------------+-------------+
                      |
                      v
               Evidence Store
                      |
                      v
              Investigation Graph
                      |
                      v
               Investigator Agent
                      |
                      v
                 Human Review
```

## Components

### API
FastAPI service exposing cases, investigations, findings, evidence, agents and graph endpoints.

### Orchestrator
Coordinates agent execution, dependencies, retries, timeouts and typed results. It must not hide tool failures.

### Evidence service
Stores immutable evidence records with source, timestamps, retrieval metadata, hashes where applicable and confidence metadata.

### Graph service
Represents relationships among Person, Organization, Account, Transaction, Device, IP, Beneficiary, Source and Evidence.

### Deterministic controls
Rules whose outputs must be reproducible: sanctions matching thresholds, velocity rules, transaction aggregation and configured AML scenarios.

### AI agents
Agents interpret retrieved data, propose hypotheses and summarize findings. They do not create facts or silently change deterministic results.

### Human review
Final consequential actions remain with the analyst.

## Initial technology direction

- Python 3.12
- FastAPI
- Pydantic
- PostgreSQL
- Neo4j
- Redis
- React + TypeScript
- Docker Compose
- OpenAI-compatible LLM abstraction
- Structured JSON outputs for agents

## Non-negotiable properties

1. Evidence provenance.
2. Audit trail.
3. Identity ambiguity is visible.
4. No autonomous accusation.
5. External-source claims preserve their source.
6. Tool failures are explicit.
7. Every finding can be traced back to evidence.
