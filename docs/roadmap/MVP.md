# MVP Roadmap

## Objective

Demonstrate a complete, explainable fictional fraud investigation from transaction ingestion to human review.

## Demo case

A fictional COP 9,800,000 transfer triggers an investigation.

The platform should discover:
- no sanctions match
- KYC inconsistency
- device shared by multiple identities
- repeated transfers in a short period
- common beneficiary network
- public-profile context
- uncertain identity resolution

## MVP agents

1. OFAC Agent
2. KYC Agent
3. Transaction / AML Agent
4. Device Agent
5. OSINT + News Agent
6. Investigator Agent

## MVP platform capabilities

- Create case
- Start investigation
- Stream agent status
- Persist evidence
- Persist findings
- Render investigation graph
- Show source provenance
- Show identity confidence
- Generate final investigation summary
- Require human disposition

## Phase 1

Foundation:
- repository structure
- API skeleton
- domain schemas
- local Docker stack
- fictional seed data

## Phase 2

Investigation engine:
- orchestration
- typed agent contracts
- deterministic rule engine
- evidence model

## Phase 3

Graph:
- Neo4j model
- relationship queries
- visual graph UI

## Phase 4

OSINT:
- source adapters
- adverse-media workflow
- identity resolution
- source-verification logic

## Phase 5

Demo experience:
- live agent activity
- investigation timeline
- analyst review screen
- video-ready scenario
