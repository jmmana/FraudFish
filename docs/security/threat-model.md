# Security and Audit Baseline

## Scope

This document defines the minimum security assumptions for the FraudFish MVP.

## Threat assumptions

FraudFish may process highly sensitive financial, identity and investigation data. The MVP therefore assumes:

- external data sources can be malicious, stale or incorrect
- LLM output can be wrong or manipulated
- public-source identity matches can refer to a namesake
- secrets can leak through logs if not explicitly redacted
- investigator actions require auditability
- graph relationships may reveal sensitive associations
- prompt injection can arrive through external content

## MVP controls

### Human authority

No agent may autonomously block an account, accuse a subject, submit a regulatory report or take another consequential enforcement action.

### Provenance

External claims must retain source references.

### Identity ambiguity

A public-source candidate remains unconfirmed until human validation.

### Secrets

Secrets belong in environment variables or a secret manager, never in source control.

### Logging

Structured audit events may include IDs and operational metadata but should not contain raw passwords, tokens, full account references or unnecessary identity data.

### External content

Retrieved web, news and social content is data, not trusted instructions. Agents must not execute instructions embedded in retrieved content.

### Test data

The public MVP uses fictional test data only.

## Future production controls

- authentication and RBAC
- tenant isolation
- encryption at rest
- encrypted secret management
- immutable audit storage
- retention policies
- source allowlists / deny lists
- prompt-injection defenses
- model/tool authorization policy
- rate limits
- case-level access controls
- regulatory data residency review
