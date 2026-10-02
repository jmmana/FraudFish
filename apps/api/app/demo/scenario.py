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
        "subject_name": "Alejandro Torres Vega",
        "subject_country": "CO",
        "subject_city": "Medellin",
        "subject_occupation": "Software Architect",
        "transactions": transactions,
        "device_links": [
            {"device_ref": "DEV-8732", "identity_ref": "DEMO-PERSON-1"},
            {"device_ref": "DEV-8732", "identity_ref": "DEMO-PERSON-2"},
            {"device_ref": "DEV-8732", "identity_ref": "DEMO-PERSON-3"},
            {"device_ref": "DEV-8732", "identity_ref": "DEMO-PERSON-4"},
            {"device_ref": "DEV-8732", "identity_ref": "DEMO-PERSON-5"},
            {"device_ref": "DEV-8732", "identity_ref": "DEMO-PERSON-6"},
        ],
    }
