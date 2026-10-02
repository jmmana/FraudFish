from app.security.redaction import redact_mapping


def test_redacts_sensitive_fields_recursively() -> None:
    payload = {
        "document_id": "123456789",
        "nested": {
            "account_ref": "9988776655",
            "safe": "visible",
        },
    }

    redacted = redact_mapping(payload)

    assert redacted["document_id"] != "123456789"
    assert redacted["nested"]["account_ref"] != "9988776655"
    assert redacted["nested"]["safe"] == "visible"
