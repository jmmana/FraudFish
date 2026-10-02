from __future__ import annotations

from app.agents.contracts import AgentContext, AgentResult, AgentStatus


SEVERITY_WEIGHT = {
    "info": 0,
    "low": 5,
    "medium": 10,
    "high": 20,
    "critical": 35,
}


class InvestigatorAgent:
    name = "investigator"

    def run(self, context: AgentContext) -> AgentResult:
        prior_results = context.inputs.get("_prior_agent_results") or []
        if not isinstance(prior_results, list):
            prior_results = []

        total_score = 0
        supporting_agents: list[str] = []
        signal_count = 0
        failed_agents: list[str] = []

        for result in prior_results:
            if not isinstance(result, dict):
                continue

            agent_name = str(result.get("agent") or "unknown")
            status = str(result.get("status") or "")
            if status == "failed":
                failed_agents.append(agent_name)
                continue

            signals = result.get("signals") or []
            if signals:
                supporting_agents.append(agent_name)

            for signal in signals:
                if not isinstance(signal, dict):
                    continue
                signal_count += 1
                severity = str(signal.get("severity") or "info").lower()
                total_score += SEVERITY_WEIGHT.get(severity, 0)

        risk_score = min(100, total_score)
        if risk_score >= 70:
            risk_band = "high"
            suggested_action = "escalate_for_human_review"
        elif risk_score >= 35:
            risk_band = "medium"
            suggested_action = "enhanced_human_review"
        else:
            risk_band = "low"
            suggested_action = "standard_human_review"

        statement = (
            f"Aggregated {signal_count} signal(s) from "
            f"{len(set(supporting_agents))} contributing agent(s). "
            f"Calculated review-priority score {risk_score}/100 ({risk_band})."
        )

        return AgentResult(
            agent=self.name,
            status=AgentStatus.SUCCEEDED,
            summary=statement,
            findings=[
                {
                    "statement": statement,
                    "confidence": 1.0,
                }
            ],
            metadata={
                "risk_score": risk_score,
                "risk_band": risk_band,
                "suggested_action": suggested_action,
                "supporting_agents": sorted(set(supporting_agents)),
                "failed_agents": sorted(set(failed_agents)),
                "human_decision_required": True,
                "autonomous_enforcement_allowed": False,
            },
        )
