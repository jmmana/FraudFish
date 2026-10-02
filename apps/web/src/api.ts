import type { DemoResponse, InvestigationGraph } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function runDemo(): Promise<DemoResponse> {
  const response = await fetch(`${API_BASE}/demo/run`, { method: "POST" });
  if (!response.ok) {
    throw new Error("Failed to run FraudFish demo");
  }
  return response.json();
}

export async function loadDemoGraph(): Promise<InvestigationGraph> {
  const response = await fetch(`${API_BASE}/graph/demo`);
  if (!response.ok) {
    throw new Error("Failed to load investigation graph");
  }
  return response.json();
}


export async function submitDecision(
  caseId: string,
  investigationId: string,
  decision: string,
  rationale: string,
  analyst: string
): Promise<unknown> {
  const response = await fetch(`${API_BASE}/cases/${caseId}/decisions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      investigation_id: investigationId,
      decision,
      rationale,
      analyst,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to record human disposition");
  }

  return response.json();
}
