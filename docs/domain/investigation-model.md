# Investigation Domain Model

## Core chain

```text
Signal -> Evidence -> Finding -> Hypothesis -> Decision
```

These objects must not be collapsed into a single risk score.

## Signal

A potentially relevant observation. Signals may be weak, noisy or unverified.

Examples:
- Name appears in a social post.
- Transaction is larger than historical median.
- Device is shared with another user.

## Evidence

A preserved observation from a known source.

Required attributes:
- source type
- source URI or internal reference
- collected timestamp
- raw or normalized value
- provenance metadata
- integrity metadata when applicable

## Finding

An agent or rule interpretation of one or more evidence items.

Examples:
- "Device is associated with six customer profiles."
- "Eight similar transfers occurred in 48 hours."

## Hypothesis

A testable investigation proposition, not a fact.

Example:
- "The activity may represent structuring."

A hypothesis must point to supporting and contradicting findings.

## Decision

A human or explicitly configured workflow action.

Examples:
- request enhanced due diligence
- request source-of-funds documentation
- close alert
- escalate case

## Identity Resolution

A name match does not establish identity.

Candidate identity matches should retain:
- matched fields
- conflicting fields
- source quality
- confidence score
- analyst confirmation state

## Source quality

FraudFish will distinguish source reliability from factual relevance.

A low-reliability source can generate a Signal, but should not automatically become a high-confidence Finding.
