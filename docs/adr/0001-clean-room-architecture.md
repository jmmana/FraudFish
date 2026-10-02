# ADR-0001 — Clean-room architecture instead of a direct MiroFish fork

**Status:** Accepted  
**Date:** 2026-10-02

## Context

MiroFish is a useful conceptual reference for multi-agent orchestration, graph memory and visualization, but its repository is licensed under AGPL-3.0 and its domain model is centered on social simulation and prediction.

FraudFish has a different product boundary: financial-crime investigation, evidence provenance, identity resolution, AML controls and human review.

## Decision

FraudFish will be implemented as an independent codebase.

We may study public architectural ideas and behavior, but we will not copy MiroFish source files into FraudFish unless we intentionally decide to accept the applicable license obligations for a specific component and document that decision separately.

## Consequences

- Domain model remains focused on investigations rather than simulated societies.
- Licensing boundaries remain explicit.
- We can choose infrastructure and agent frameworks based on FraudFish requirements.
- Reusing third-party code requires a new ADR and license review.
