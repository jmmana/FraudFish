from __future__ import annotations

from app.agents.contracts import AgentContext, AgentResult, AgentStatus


RELIABILITY_WEIGHT = {
    "low": 0.25,
    "medium": 0.50,
    "high": 0.80,
    "authoritative": 1.00,
}


class SourceVerificationAgent:
    name = "source_verification"

    def run(self, context: AgentContext) -> AgentResult:
        prior_results = context.inputs.get("_prior_agent_results") or []
        reviewed = []
        low_reliability = []
        authoritative = []

        for result in prior_results:
            if not isinstance(result, dict):
                continue
            for evidence in result.get("evidence") or []:
                if not isinstance(evidence, dict):
                    continue

                source_type = str(evidence.get("source_type") or "unknown")
                source_ref = str(evidence.get("source_ref") or "")
                reliability = str(evidence.get("reliability") or "low").lower()
                weight = RELIABILITY_WEIGHT.get(reliability, 0.25)

                item = {
                    "source_type": source_type,
                    "source_ref": source_ref,
                    "reliability": reliability,
                    "weight": weight,
                }
                reviewed.append(item)

                if reliability == "low":
                    low_reliability.append(item)
                if reliability == "authoritative":
                    authoritative.append(item)

        signals = []
        if low_reliability:
            signals.append(
                {
                    "signal_type": "low_reliability_sources_present",
                    "severity": "info",
                    "summary": (
                        f"{len(low_reliability)} low-reliability evidence item(s) require "
                        "corroboration before consequential use."
                    ),
                }
            )

        return AgentResult(
            agent=self.name,
            status=AgentStatus.SUCCEEDED,
            summary=f"Verified provenance metadata for {len(reviewed)} evidence item(s).",
            signals=signals,
            findings=[
                {
                    "statement": (
                        f"Evidence set contains {len(authoritative)} authoritative and "
                        f"{len(low_reliability)} low-reliability source item(s)."
                    ),
                    "confidence": 1.0,
                }
            ],
            metadata={
                "reviewed_count": len(reviewed),
                "authoritative_count": len(authoritative),
                "low_reliability_count": len(low_reliability),
                "policy": "low-reliability evidence requires corroboration",
            },
        )
