from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any


def build_demo_investigation_input() -> dict[str, Any]:
    now = datetime.now(timezone.utc)

    transactions = [
        {
            "transaction_ref": f"DEMO-TX-{index + 1:02d}",
            "amount": 9_800_000,
            "occurred_at": (now - timedelta(hours=index * 4)).isoformat(),
            "beneficiary_ref": "BEN-4421",
        }
        for index in range(8)
    ]

    return {
        "subject_name": "Juan Manuel Castillo Pinto",
        "subject_country": "CO",
        "subject_city": "Medellin",
        "subject_occupation": "Software Architect",
        "transactions": transactions,
    }
