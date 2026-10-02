from __future__ import annotations

from app.agents.contracts import AgentContext, AgentResult, AgentStatus
from app.connectors.osint import DemoOsintConnector
from app.services.identity_resolution import (
    IdentityResolutionInput,
    resolve_candidate,
)


class OsintIdentityAgent:
    name = "osint_identity"

    def __init__(self, connector: DemoOsintConnector | None = None) -> None:
        self.connector = connector or DemoOsintConnector()

    def run(self, context: AgentContext) -> AgentResult:
        subject_name = str(context.inputs.get("subject_name") or "").strip()
        if not subject_name:
            return AgentResult(
                agent=self.name,
                status=AgentStatus.SUCCEEDED,
                summary="OSINT identity resolution skipped because no subject name was provided.",
                metadata={"screened": False, "reason": "missing_subject_name"},
            )

        subject = IdentityResolutionInput(
            full_name=subject_name,
            country=context.inputs.get("subject_country"),
            city=context.inputs.get("subject_city"),
            occupation=context.inputs.get("subject_occupation"),
            organization=context.inputs.get("subject_organization"),
        )

        records = self.connector.search_name(subject_name)
        candidates = [resolve_candidate(subject, record) for record in records]
        candidates.sort(key=lambda item: item.confidence, reverse=True)

        evidence = [
            {
                "source_type": candidate.source_type,
                "source_ref": candidate.source_ref,
                "reliability": candidate.reliability,
                "payload": {
                    "candidate_name": candidate.candidate_name,
                    "identity_confidence": candidate.confidence,
                    "matched_fields": list(candidate.matched_fields),
                    "conflicting_fields": list(candidate.conflicting_fields),
                },
            }
            for candidate in candidates
        ]

        findings = []
        if candidates:
            top = candidates[0]
            findings.append({
                "statement": (
                    f"Top public-source identity candidate scored {top.confidence:.0%}; "
                    "candidate identity requires human validation."
                ),
                "confidence": top.confidence,
            })

        social_signal_count = sum(1 for item in candidates if item.source_type == "social")

        return AgentResult(
            agent=self.name,
            status=AgentStatus.SUCCEEDED,
            summary=f"Found {len(candidates)} public-source identity candidate(s).",
            signals=[
                {
                    "signal_type": "public_identity_candidate",
                    "severity": "info",
                    "summary": (
                        f"{candidate.candidate_name} candidate from {candidate.source_type} "
                        f"scored {candidate.confidence:.0%}."
                    ),
                }
                for candidate in candidates
            ],
            evidence=evidence,
            findings=findings,
            metadata={
                "screened": True,
                "candidate_count": len(candidates),
                "social_signal_count": social_signal_count,
                "identity_confirmed": False,
                "human_validation_required": True,
            },
        )
