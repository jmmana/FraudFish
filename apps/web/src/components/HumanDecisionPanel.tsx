import { FormEvent, useState } from "react";

import { submitDecision } from "../api";
import type { DemoResponse } from "../types";

type Props = {
  demo: DemoResponse | null;
};

export function HumanDecisionPanel({ demo }: Props) {
  const [decision, setDecision] = useState("escalate");
  const [rationale, setRationale] = useState("");
  const [analyst, setAnalyst] = useState("demo-analyst");
  const [message, setMessage] = useState("");
  const [saving, setSaving] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (!demo) return;

    setSaving(true);
    setMessage("");
    try {
      await submitDecision(
        demo.case.id,
        demo.investigation.id,
        decision,
        rationale,
        analyst
      );
      setMessage("Human disposition recorded.");
    } catch (error) {
      setMessage(String(error));
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="panel decision-panel">
      <div className="panel-title">
        <div>
          <span className="muted">HUMAN-IN-THE-LOOP</span>
          <h2>Analyst disposition</h2>
        </div>
      </div>

      <form onSubmit={onSubmit}>
        <label>
          Decision
          <select
            value={decision}
            onChange={(event) => setDecision(event.target.value)}
            disabled={!demo}
          >
            <option value="escalate">Escalate</option>
            <option value="request_edd">Request enhanced due diligence</option>
            <option value="request_source_of_funds">Request source of funds</option>
            <option value="request_source_of_wealth">Request source of wealth</option>
            <option value="close">Close alert</option>
          </select>
        </label>

        <label>
          Analyst
          <input
            value={analyst}
            onChange={(event) => setAnalyst(event.target.value)}
            disabled={!demo}
          />
        </label>

        <label>
          Rationale
          <textarea
            value={rationale}
            onChange={(event) => setRationale(event.target.value)}
            placeholder="Explain the human decision..."
            disabled={!demo}
            required
            minLength={3}
          />
        </label>

        <button type="submit" disabled={!demo || saving || rationale.length < 3}>
          {saving ? "Saving…" : "Record disposition"}
        </button>
      </form>

      {message && <p className="decision-message">{message}</p>}
    </section>
  );
}
