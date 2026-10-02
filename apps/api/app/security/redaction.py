from __future__ import annotations

import re
from typing import Any


SENSITIVE_KEYS = {
    "document_id",
    "account_ref",
    "api_key",
    "access_token",
    "authorization",
    "password",
    "secret",
}


def redact_value(value: str) -> str:
    if len(value) <= 4:
        return "***"
    return f"{value[:2]}***{value[-2:]}"


def redact_mapping(payload: dict[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}

    for key, value in payload.items():
        normalized = key.lower()
        if normalized in SENSITIVE_KEYS:
            redacted[key] = redact_value(str(value))
        elif isinstance(value, dict):
            redacted[key] = redact_mapping(value)
        elif isinstance(value, list):
            redacted[key] = [
                redact_mapping(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            redacted[key] = value

    return redacted
