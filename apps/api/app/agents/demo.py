from app.agents.contracts import AgentContext, AgentResult, AgentStatus


class DemoOFACAgent:
    name = "ofac"

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent=self.name,
            status=AgentStatus.SUCCEEDED,
            summary="No sanctions match found in fictional demo data.",
            evidence=[
                {
                    "source_type": "sanctions",
                    "source_ref": "fixture://ofac/demo",
                    "reliability": "authoritative",
                    "corroborated": True,
                }
            ],
            findings=[
                {
                    "statement": "No sanctions candidate exceeded the configured match threshold.",
                    "confidence": 1.0,
                }
            ],
            metadata={"deterministic": True, "demo": True},
        )


class DemoKycAgent:
    name = "kyc"

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent=self.name,
            status=AgentStatus.SUCCEEDED,
            summary="Declared profile is inconsistent with observed transaction volume.",
            signals=[
                {
                    "signal_type": "kyc_volume_mismatch",
                    "severity": "high",
                    "summary": "Observed volume exceeds fictional expected profile.",
                }
            ],
            findings=[
                {
                    "statement": "Transaction activity is materially above the fictional customer profile.",
                    "confidence": 0.93,
                }
            ],
            metadata={"demo": True},
        )
