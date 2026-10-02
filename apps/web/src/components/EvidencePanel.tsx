import { useMemo, useState } from "react";

import type { AgentResult } from "../types";

type Props = {
  agents: AgentResult[];
};

type EvidenceItem = {
  agent: string;
  source_type?: string;
  source_ref?: string;
  reliability?: string;
  payload?: unknown;
};

export function EvidencePanel({ agents }: Props) {
  const items = useMemo<EvidenceItem[]>(
    () =>
      agents.flatMap((agent) =>
        agent.evidence.map((evidence) => ({
          agent: agent.agent,
          source_type: String(evidence.source_type ?? ""),
          source_ref: String(evidence.source_ref ?? ""),
          reliability: String(evidence.reliability ?? ""),
          payload: evidence.payload,
        }))
      ),
    [agents]
  );

  const [selectedIndex, setSelectedIndex] = useState(0);
  const selected = items[selectedIndex];

  return (
    <section className="panel evidence-panel">
      <div className="panel-title">
        <div>
          <span className="muted">PROVENANCE</span>
          <h2>Evidence</h2>
        </div>
        <span className="muted">{items.length} item(s)</span>
      </div>

      {items.length === 0 ? (
        <p className="empty-copy">Run an investigation to inspect evidence and source provenance.</p>
      ) : (
        <div className="evidence-layout">
          <div className="evidence-list">
            {items.map((item, index) => (
              <button
                className={`evidence-row ${index === selectedIndex ? "active" : ""}`}
                key={`${item.agent}-${item.source_ref}-${index}`}
                onClick={() => setSelectedIndex(index)}
              >
                <span>{item.agent}</span>
                <strong>{item.source_type || "source"}</strong>
                <small>{item.reliability || "unknown reliability"}</small>
              </button>
            ))}
          </div>

          <div className="evidence-detail">
            <span className="muted">SOURCE REFERENCE</span>
            <p className="source-ref">{selected?.source_ref || "—"}</p>

            <span className="muted">PAYLOAD</span>
            <pre>{JSON.stringify(selected?.payload ?? {}, null, 2)}</pre>
          </div>
        </div>
      )}
    </section>
  );
}
