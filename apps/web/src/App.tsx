import { useEffect, useMemo, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";

import { loadDemoGraph, runDemo } from "./api";
import { EvidencePanel } from "./components/EvidencePanel";
import { HumanDecisionPanel } from "./components/HumanDecisionPanel";
import type { AgentResult, DemoResponse, GraphNode, InvestigationGraph } from "./types";

const labelForAgent = (agent: string) =>
  ({
    ofac: "OFAC",
    kyc: "KYC",
    aml: "AML",
    device: "Device",
    osint_identity: "OSINT / Identity",
    investigator: "Investigator",
  })[agent] ?? agent;

function App() {
  const [demo, setDemo] = useState<DemoResponse | null>(null);
  const [graph, setGraph] = useState<InvestigationGraph | null>(null);
  const [selected, setSelected] = useState<GraphNode | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDemoGraph().then(setGraph).catch((err) => setError(String(err)));
  }, []);

  const graphData = useMemo(() => {
    if (!graph) return { nodes: [], links: [] };
    return {
      nodes: graph.nodes.map((node) => ({ ...node })),
      links: graph.edges.map((edge) => ({
        ...edge,
        source: edge.source,
        target: edge.target,
      })),
    };
  }, [graph]);

  const execute = async () => {
    setLoading(true);
    setError("");
    try {
      const result = await runDemo();
      setDemo(result);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">MULTI-AGENT FINANCIAL CRIME INVESTIGATION</p>
          <h1>FraudFish</h1>
        </div>
        <button onClick={execute} disabled={loading}>
          {loading ? "Investigating…" : "Run investigation"}
        </button>
      </header>

      {error && <div className="error">{error}</div>}

      <section className="case-card">
        <div>
          <span className="muted">CASE</span>
          <strong>{demo?.case.case_ref ?? "FR-2026-1042"}</strong>
        </div>
        <div>
          <span className="muted">SUBJECT</span>
          <strong>Alejandro Torres Vega</strong>
        </div>
        <div>
          <span className="muted">TRANSACTION</span>
          <strong>$9,800,000 COP</strong>
        </div>
        <div>
          <span className="muted">REVIEW</span>
          <strong>{demo ? "Human required" : "Pending"}</strong>
        </div>
      </section>

      <section className="layout">
        <div className="panel agents-panel">
          <div className="panel-title">
            <div>
              <span className="muted">LIVE INVESTIGATION</span>
              <h2>Agent activity</h2>
            </div>
            <span className="status-pill">{demo?.investigation.status ?? "ready"}</span>
          </div>

          <div className="agent-grid">
            {(demo?.agents ?? [
              { agent: "ofac", status: "queued", summary: "Sanctions screening", signals: [], evidence: [], findings: [], metadata: {} },
              { agent: "kyc", status: "queued", summary: "Customer profile consistency", signals: [], evidence: [], findings: [], metadata: {} },
              { agent: "aml", status: "queued", summary: "Transaction pattern analysis", signals: [], evidence: [], findings: [], metadata: {} },
              { agent: "device", status: "queued", summary: "Shared-device relationship analysis", signals: [], evidence: [], findings: [], metadata: {} },
              { agent: "osint_identity", status: "queued", summary: "Public-source identity resolution", signals: [], evidence: [], findings: [], metadata: {} },
              { agent: "investigator", status: "queued", summary: "Evidence synthesis and review prioritization", signals: [], evidence: [], findings: [], metadata: {} },
            ] as AgentResult[]).map((agent) => (
              <article className="agent-card" key={agent.agent}>
                <div className="agent-head">
                  <strong>{labelForAgent(agent.agent)}</strong>
                  <span className={`agent-state ${agent.status}`}>{agent.status}</span>
                </div>
                <p>{agent.summary}</p>
                {agent.signals.length > 0 && (
                  <div className="signal-count">{agent.signals.length} signal(s)</div>
                )}
              </article>
            ))}
          </div>
        </div>

        <aside className="panel risk-panel">
          <span className="muted">CASE ASSESSMENT</span>
          <div className="risk-score">
            {demo
              ? String(
                  demo.agents.find((a) => a.agent === "investigator")?.metadata.risk_band ?? "—"
                ).toUpperCase()
              : "—"}
          </div>
          <p>
            FraudFish exposes evidence and hypotheses; the final disposition remains with the analyst.
          </p>
          <div className="rule">
            <span>Human review</span>
            <strong>{demo ? "Required" : "Pending"}</strong>
          </div>
          <div className="rule">
            <span>OSINT identity</span>
            <strong>{demo ? "Unconfirmed" : "Pending"}</strong>
          </div>
          <div className="rule">
            <span>AML signals</span>
            <strong>
              {demo
                ? demo.agents.find((a) => a.agent === "aml")?.signals.length ?? 0
                : 0}
            </strong>
          </div>
        </aside>
      </section>

      <EvidencePanel agents={demo?.agents ?? []} />

      <HumanDecisionPanel demo={demo} />

      <section className="panel graph-panel">
        <div className="panel-title">
          <div>
            <span className="muted">RELATIONSHIP INTELLIGENCE</span>
            <h2>Investigation graph</h2>
          </div>
          <span className="muted">Click a node to inspect it</span>
        </div>

        <div className="graph-layout">
          <div className="graph-canvas">
            <ForceGraph2D
              graphData={graphData}
              width={860}
              height={520}
              nodeAutoColorBy="type"
              nodeLabel={(node: any) => `${node.label} · ${node.type}`}
              linkDirectionalArrowLength={4}
              linkDirectionalArrowRelPos={1}
              onNodeClick={(node: any) => setSelected(node as GraphNode)}
            />
          </div>

          <aside className="node-inspector">
            <span className="muted">NODE INSPECTOR</span>
            {selected ? (
              <>
                <h3>{selected.label}</h3>
                <p className="node-type">{selected.type}</p>
                <dl>
                  {Object.entries(selected.properties).map(([key, value]) => (
                    <div key={key}>
                      <dt>{key}</dt>
                      <dd>{String(value)}</dd>
                    </div>
                  ))}
                </dl>
              </>
            ) : (
              <p>Select a person, device, transaction, source or beneficiary to inspect its context.</p>
            )}
          </aside>
        </div>
      </section>
    </main>
  );
}

export default App;
