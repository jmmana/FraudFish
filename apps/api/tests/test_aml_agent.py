from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.agents.aml import TransactionAmlAgent
from app.agents.contracts import AgentContext


def build_context(transactions: list[dict]) -> AgentContext:
    return AgentContext(
        case_id=uuid4(),
        investigation_id=uuid4(),
        trace_id=uuid4(),
        inputs={"transactions": transactions},
    )


def test_aml_agent_detects_velocity_and_common_beneficiary() -> None:
    now = datetime.now(timezone.utc)
    transactions = [
        {
            "transaction_ref": f"TX-{index}",
            "amount": 9800000,
            "occurred_at": (now - timedelta(hours=index * 4)).isoformat(),
            "beneficiary_ref": "BEN-4421",
        }
        for index in range(8)
    ]

    result = TransactionAmlAgent().run(build_context(transactions))

    signal_types = {item["signal_type"] for item in result.signals}
    assert "high_velocity" in signal_types
    assert "common_beneficiary" in signal_types
    assert "repeated_amount_pattern" in signal_types


def test_aml_agent_detects_large_amount_deviation() -> None:
    now = datetime.now(timezone.utc)
    transactions = [
        {
            "transaction_ref": "HIST-1",
            "amount": 1000000,
            "occurred_at": (now - timedelta(days=10)).isoformat(),
            "beneficiary_ref": "A",
        },
        {
            "transaction_ref": "HIST-2",
            "amount": 1200000,
            "occurred_at": (now - timedelta(days=8)).isoformat(),
            "beneficiary_ref": "B",
        },
        {
            "transaction_ref": "CURRENT",
            "amount": 9800000,
            "occurred_at": now.isoformat(),
            "beneficiary_ref": "C",
        },
    ]

    result = TransactionAmlAgent().run(build_context(transactions))
    signal_types = {item["signal_type"] for item in result.signals}

    assert "amount_deviation" in signal_types
