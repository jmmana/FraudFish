from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher


def normalize_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    without_marks = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    compact = re.sub(r"[^a-zA-Z0-9 ]+", " ", without_marks).lower()
    return " ".join(compact.split())


def similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, normalize_name(left), normalize_name(right)).ratio()


@dataclass(frozen=True)
class NameMatch:
    candidate_name: str
    normalized_candidate: str
    score: float
    exact: bool


def best_name_match(query: str, candidates: list[str]) -> NameMatch | None:
    if not candidates:
        return None

    normalized_query = normalize_name(query)
    ranked = []
    for candidate in candidates:
        normalized_candidate = normalize_name(candidate)
        ranked.append(
            NameMatch(
                candidate_name=candidate,
                normalized_candidate=normalized_candidate,
                score=similarity(query, candidate),
                exact=normalized_query == normalized_candidate,
            )
        )

    return max(ranked, key=lambda item: item.score)
