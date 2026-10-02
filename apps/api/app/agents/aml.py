from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta
from statistics import median
from typing import Any

from app.agents.contracts import AgentContext, AgentResult, AgentStatus


class TransactionAmlAgent:
    name = "aml"

    def __init__(
        self,
        velocity_window_hours: int = 48,
        repeated_transfer_count: int = 5,
        amount_deviation_multiplier: float = 4.0,
    ) -> None:
        self.velocity_window_hours = velocity_window_hours
        self.repeated_transfer_count = repeated_transfer_count
        self.amount_deviation_multiplier = amount_deviation_multiplier

    def run(self, context: AgentContext) -> AgentResult:
        raw_transactions = context.inputs.get("transactions") or []
        if not isinstance(raw_transactions, list) or not raw_transactions:
            return AgentResult(
                agent=self.name,
                status=AgentStatus.SUCCEEDED,
                summary="AML analysis skipped because no transaction history was provided.",
                metadata={"deterministic": True, "analyzed": False},
            )

        transactions = [self._normalize_transaction(item) for item in raw_transactions]
        transactions = [item for item in transactions if item is not None]

        if not transactions:
            return AgentResult(
                agent=self.name,
                status=AgentStatus.SUCCEEDED,
                summary="No valid transactions were available for AML analysis.",
                metadata={"deterministic": True, "analyzed": False},
            )

        transactions.sort(key=lambda item: item["occurred_at"])
        newest = transactions[-1]["occurred_at"]
        window_start = newest - timedelta(hours=self.velocity_window_hours)
        recent = [item for item in transactions if item["occurred_at"] >= window_start]

        signals: list[dict[str, Any]] = []
        findings: list[dict[str, Any]] = []

        if len(recent) >= self.repeated_transfer_count:
            signals.append({
                "signal_type": "high_velocity",
                "severity": "high",
                "summary": f"{len(recent)} transactions occurred within {self.velocity_window_hours} hours.",
            })
            findings.append({
                "statement": f"Transaction velocity reached {len(recent)} operations in {self.velocity_window_hours} hours.",
                "confidence": 1.0,
            })

        beneficiary_counts = Counter(
            item["beneficiary_ref"]
            for item in recent
            if item.get("beneficiary_ref")
        )
        if beneficiary_counts:
            beneficiary, count = beneficiary_counts.most_common(1)[0]
            if count >= self.repeated_transfer_count:
                signals.append({
                    "signal_type": "common_beneficiary",
                    "severity": "high",
                    "summary": f"{count} recent transfers share beneficiary {beneficiary}.",
                })
                findings.append({
                    "statement": f"Beneficiary {beneficiary} received {count} transfers in the analysis window.",
                    "confidence": 1.0,
                })

        amounts = [item["amount"] for item in transactions[:-1] if item["amount"] > 0]
        latest_amount = transactions[-1]["amount"]
        if amounts:
            baseline = median(amounts)
            if baseline > 0:
                multiplier = latest_amount / baseline
                if multiplier >= self.amount_deviation_multiplier:
                    signals.append({
                        "signal_type": "amount_deviation",
                        "severity": "high",
                        "summary": f"Latest amount is {multiplier:.2f}x the historical median.",
                    })
                    findings.append({
                        "statement": f"Latest transaction amount is {multiplier:.2f} times the historical median.",
                        "confidence": 1.0,
                    })

        repeated_amounts = Counter(round(item["amount"], 2) for item in recent)
        repeated_amount_count = max(repeated_amounts.values()) if repeated_amounts else 0
        if repeated_amount_count >= self.repeated_transfer_count:
            amount, count = repeated_amounts.most_common(1)[0]
            signals.append({
                "signal_type": "repeated_amount_pattern",
                "severity": "medium",
                "summary": f"{count} transfers used the same amount {amount:.2f}.",
            })
            findings.append({
                "statement": f"{count} transfers repeated the exact amount {amount:.2f} in the analysis window.",
                "confidence": 1.0,
            })

        summary = (
            f"AML analysis produced {len(signals)} deterministic signal(s)."
            if signals
            else "No configured AML rule triggered."
        )

        return AgentResult(
            agent=self.name,
            status=AgentStatus.SUCCEEDED,
            summary=summary,
            signals=signals,
            evidence=[{
                "source_type": "transaction",
                "source_ref": "input://investigation/transactions",
                "reliability": "high",
                "payload": {
                    "transaction_count": len(transactions),
                    "window_transaction_count": len(recent),
                    "window_hours": self.velocity_window_hours,
                },
            }],
            findings=findings,
            metadata={
                "deterministic": True,
                "analyzed": True,
                "rules": [
                    "high_velocity",
                    "common_beneficiary",
                    "amount_deviation",
                    "repeated_amount_pattern",
                ],
            },
        )

    @staticmethod
    def _normalize_transaction(item: Any) -> dict[str, Any] | None:
        if not isinstance(item, dict):
            return None

        try:
            amount = float(item["amount"])
            occurred_at = datetime.fromisoformat(str(item["occurred_at"]).replace("Z", "+00:00"))
        except (KeyError, TypeError, ValueError):
            return None

        return {
            "amount": amount,
            "occurred_at": occurred_at,
            "beneficiary_ref": item.get("beneficiary_ref"),
            "transaction_ref": item.get("transaction_ref"),
        }
