from __future__ import annotations

from app.agents.contracts import AgentContext, AgentResult, AgentStatus


class DeviceAgent:
    name = "device"

    def __init__(self, high_risk_identity_count: int = 4) -> None:
        self.high_risk_identity_count = high_risk_identity_count

    def run(self, context: AgentContext) -> AgentResult:
        links = context.inputs.get("device_links") or []
        if not isinstance(links, list) or not links:
            return AgentResult(
                agent=self.name,
                status=AgentStatus.SUCCEEDED,
                summary="Device analysis skipped because no device relationship data was provided.",
                metadata={"deterministic": True, "analyzed": False},
            )

        by_device: dict[str, set[str]] = {}
        for item in links:
            if not isinstance(item, dict):
                continue
            device_ref = str(item.get("device_ref") or "").strip()
            identity_ref = str(item.get("identity_ref") or "").strip()
            if not device_ref or not identity_ref:
                continue
            by_device.setdefault(device_ref, set()).add(identity_ref)

        signals = []
        findings = []
        for device_ref, identities in sorted(by_device.items()):
            identity_count = len(identities)
            if identity_count >= self.high_risk_identity_count:
                signals.append(
                    {
                        "signal_type": "shared_device",
                        "severity": "high",
                        "summary": f"Device {device_ref} is associated with {identity_count} identities.",
                    }
                )
                findings.append(
                    {
                        "statement": f"Device {device_ref} is linked to {identity_count} distinct identity references.",
                        "confidence": 1.0,
                    }
                )

        return AgentResult(
            agent=self.name,
            status=AgentStatus.SUCCEEDED,
            summary=(
                f"Device analysis produced {len(signals)} high-risk signal(s)."
                if signals
                else "No configured device-sharing rule triggered."
            ),
            signals=signals,
            evidence=[
                {
                    "source_type": "device",
                    "source_ref": "input://investigation/device-links",
                    "reliability": "high",
                    "payload": {
                        "device_count": len(by_device),
                        "relationship_count": sum(len(v) for v in by_device.values()),
                    },
                }
            ],
            findings=findings,
            metadata={
                "deterministic": True,
                "analyzed": True,
                "high_risk_identity_count": self.high_risk_identity_count,
            },
        )
