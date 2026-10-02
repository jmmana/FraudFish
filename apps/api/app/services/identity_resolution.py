from __future__ import annotations

from dataclasses import dataclass, field

from app.connectors.osint import PublicProfileRecord
from app.services.name_matching import similarity


@dataclass(frozen=True)
class IdentityResolutionInput:
    full_name: str
    country: str | None = None
    city: str | None = None
    occupation: str | None = None
    organization: str | None = None


@dataclass(frozen=True)
class IdentityResolutionResult:
    source_ref: str
    source_type: str
    candidate_name: str
    confidence: float
    matched_fields: tuple[str, ...] = field(default_factory=tuple)
    conflicting_fields: tuple[str, ...] = field(default_factory=tuple)
    reliability: str = "medium"


def resolve_candidate(
    subject: IdentityResolutionInput,
    record: PublicProfileRecord,
) -> IdentityResolutionResult:
    matched: list[str] = []
    conflicting: list[str] = []

    name_score = similarity(subject.full_name, record.full_name)
    if name_score >= 0.90:
        matched.append("full_name")
    elif name_score < 0.65:
        conflicting.append("full_name")

    comparisons = (
        ("country", subject.country, record.country),
        ("city", subject.city, record.city),
        ("occupation", subject.occupation, record.occupation),
        ("organization", subject.organization, record.organization),
    )

    comparable_count = 0
    contextual_matches = 0

    for field_name, expected, actual in comparisons:
        if not expected or not actual:
            continue

        comparable_count += 1
        if similarity(str(expected), str(actual)) >= 0.85:
            matched.append(field_name)
            contextual_matches += 1
        else:
            conflicting.append(field_name)

    base = name_score * 0.60
    if comparable_count:
        base += (contextual_matches / comparable_count) * 0.40
    else:
        base += 0.10

    conflict_penalty = min(0.45, len(conflicting) * 0.15)
    confidence = max(0.0, min(1.0, base - conflict_penalty))

    return IdentityResolutionResult(
        source_ref=record.source_ref,
        source_type=record.source_type,
        candidate_name=record.full_name,
        confidence=round(confidence, 4),
        matched_fields=tuple(matched),
        conflicting_fields=tuple(conflicting),
        reliability=record.reliability,
    )
