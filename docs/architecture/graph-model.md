# Investigation Graph Model

FraudFish uses a graph to expose relationships that are difficult to see in flat transaction tables.

## Node types

- Person
- Organization
- Account
- Transaction
- Device
- IP
- Beneficiary
- Source
- Evidence
- Finding
- Case

## Core relationships

```text
(Person)-[:OWNS]->(Account)
(Person)-[:USED]->(Device)
(Device)-[:OBSERVED_FROM]->(IP)
(Account)-[:SENT]->(Transaction)
(Transaction)-[:TO]->(Beneficiary)
(Beneficiary)-[:RESOLVES_TO]->(Person|Organization|Account)
(Evidence)-[:SUPPORTS]->(Finding)
(Finding)-[:ABOUT]->(Person|Account|Transaction|Device|Beneficiary)
(Case)-[:CONTAINS]->(Evidence|Finding|Transaction)
```

## Design rules

1. Graph edges must represent observed or derived relationships with provenance.
2. Derived relationships must record which evidence or rule created them.
3. Identity-candidate edges are not equivalent to confirmed identity.
4. Public-source profiles use candidate relationships until a human validates them.
5. Graph visualization must distinguish observed facts, deterministic derivations and AI hypotheses.

## MVP demo target

The fictional demo should expose:
- one subject person
- one device connected to six identities
- eight transactions
- one beneficiary shared by fourteen senders
- OSINT identity candidates
- OFAC screening evidence
