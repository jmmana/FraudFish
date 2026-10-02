from __future__ import annotations

from app.agents.contracts import AgentContext, AgentResult, AgentStatus
from app.connectors.ofac import DemoOfacConnector, OfacConnector
from app.services.name_matching import best_name_match


class OfacAgent:
    name = "ofac"

    def __init__(
        self,
        connector: OfacConnector | None = None,
        fuzzy_threshold: float = 0.90,
    ) -> None:
        self.connector = connector or DemoOfacConnector()
        self.fuzzy_threshold = fuzzy_threshold

    def run(self, context: AgentContext) -> AgentResult:
        subject_name = str(context.inputs.get("subject_name") or "").strip()
        if not subject_name:
            return AgentResult(
                agent=self.name,
                status=AgentStatus.SUCCEEDED,
                summary="OFAC screening skipped because no subject name was provided.",
                metadata={
                    "deterministic": True,
                    "screened": False,
                    "reason": "missing_subject_name",
                },
            )

        matches = []
        for record in self.connector.list_records():
            names = [record.full_name, *record.aliases]
            best = best_name_match(subject_name, names)
            if best is None:
                continue

            matched = best.exact or best.score >= self.fuzzy_threshold
            matches.append(
                {
                    "record_uid": record.uid,
                    "matched_name": best.candidate_name,
                    "score": round(best.score, 4),
                    "exact": best.exact,
                    "matched": matched,
                    "date_of_birth": record.date_of_birth,
                    "nationality": record.nationality,
                    "source_ref": record.source_ref,
                }
            )

        positive_matches = [item for item in matches if item["matched"]]
        top = max(matches, key=lambda item: item["score"]) if matches else None

        if positive_matches:
            return AgentResult(
                agent=self.name,
                status=AgentStatus.SUCCEEDED,
                summary=f"{len(positive_matches)} sanctions candidate(s) exceeded the configured threshold.",
                evidence=[
                    {
                        "source_type": "sanctions",
                        "source_ref": item["source_ref"],
                        "reliability": "authoritative",
                        "payload": item,
                    }
                    for item in positive_matches
                ],
                findings=[
                    {
                        "statement": "A sanctions name candidate exceeded the deterministic match threshold; identity is not confirmed by name match alone.",
                        "confidence": max(item["score"] for item in positive_matches),
                    }
                ],
                metadata={
                    "deterministic": True,
                    "screened": True,
                    "threshold": self.fuzzy_threshold,
                    "candidate_count": len(matches),
                    "positive_match_count": len(positive_matches),
                },
            )

        return AgentResult(
            agent=self.name,
            status=AgentStatus.SUCCEEDED,
            summary="No sanctions candidate exceeded the configured match threshold.",
            evidence=[
                {
                    "source_type": "sanctions",
                    "source_ref": "fixture://ofac/demo",
                    "reliability": "authoritative",
                    "payload": {"top_candidate": top},
                }
            ],
            findings=[
                {
                    "statement": "No sanctions candidate exceeded the configured deterministic name-match threshold.",
                    "confidence": 1.0,
                }
            ],
            metadata={
                "deterministic": True,
                "screened": True,
                "threshold": self.fuzzy_threshold,
                "candidate_count": len(matches),
                "positive_match_count": 0,
            },
        )
