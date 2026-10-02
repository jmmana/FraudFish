# FraudFish

**Multi-Agent AI Platform for Fraud, AML, OSINT and Financial Crime Investigation**

FraudFish is an explainable investigation platform that coordinates deterministic controls, specialized AI agents, OSINT, transaction intelligence and graph analysis to help human analysts investigate suspicious financial activity.

> **Human-in-the-loop by design.** FraudFish does not autonomously accuse, convict or make final compliance decisions. It gathers signals, preserves evidence, explains findings and helps investigators prioritize cases.

## Vision

A suspicious transaction should not be evaluated by one generic AI model. FraudFish treats an investigation as a team effort:

- Sanctions / OFAC screening
- PEP and watchlist screening
- KYC consistency analysis
- Transaction and AML pattern analysis
- Device / IP intelligence
- Network and relationship analysis
- OSINT and adverse-media research
- Identity resolution
- Source verification
- Investigator synthesis

Every conclusion must be traceable to a **source, deterministic rule, observation or agent finding**.

## Core model

```text
Signal -> Evidence -> Finding -> Hypothesis -> Human Decision
```

FraudFish explicitly separates these concepts so that unverified public information is never treated as proven fact.

## Initial MVP

The first vertical slice will demonstrate one fictional suspicious-transfer investigation using:

1. OFAC Agent
2. KYC Agent
3. Transaction / AML Agent
4. Device Agent
5. OSINT + News Agent
6. Investigator Agent
7. Investigation Graph

The demo will show live agent activity, evidence provenance, identity-match uncertainty and a graph connecting people, accounts, devices, IPs and beneficiaries.

## Architecture direction

- **Backend:** Python 3.12 + FastAPI
- **Frontend:** React + TypeScript
- **Relational data:** PostgreSQL
- **Investigation graph:** Neo4j
- **Cache / coordination:** Redis
- **Runtime:** Docker Compose for local development
- **LLMs:** provider-neutral OpenAI-compatible abstraction
- **Agent execution:** explicit tool-calling with typed outputs
- **Observability:** structured logs + trace IDs per investigation

See [docs/architecture/overview.md](docs/architecture/overview.md).

## Project principles

- Evidence before inference.
- Provenance for every external claim.
- Identity resolution is probabilistic, never assumed from a name match.
- Deterministic controls remain deterministic.
- LLMs interpret evidence; they do not manufacture it.
- Social-media findings are signals unless independently corroborated.
- Human review is required for consequential actions.
- Test data first; no production PII in the MVP.
- Security and auditability are product features, not afterthoughts.

## MiroFish relationship

FraudFish is **not a code fork** of MiroFish.

MiroFish is an important conceptual reference for multi-agent orchestration, graph memory and visualization. Its repository is licensed under AGPL-3.0. FraudFish starts as a clean-room implementation with its own domain model and codebase so licensing and domain boundaries remain explicit.

See [ADR-0001](docs/adr/0001-clean-room-architecture.md).

## Repository

```text
apps/
  api/
  web/
agents/
connectors/
domain/
services/
docs/
  adr/
  architecture/
  domain/
  roadmap/
tests/
```

## Status

**Phase 0 — Foundation**

The repository is being initialized around the first end-to-end investigation demo.

---

FraudFish is an experimental research and engineering project. It is not legal, regulatory or compliance advice.
