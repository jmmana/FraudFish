export type AgentResult = {
  agent: string;
  status: string;
  summary: string;
  signals: Array<Record<string, unknown>>;
  evidence: Array<Record<string, unknown>>;
  findings: Array<Record<string, unknown>>;
  metadata: Record<string, unknown>;
};

export type DemoResponse = {
  case: {
    id: string;
    case_ref: string;
    title: string;
    status: string;
  };
  investigation: {
    id: string;
    trace_id: string;
    status: string;
  };
  agents: AgentResult[];
  human_review_required: boolean;
};

export type GraphNode = {
  id: string;
  type: string;
  label: string;
  properties: Record<string, unknown>;
};

export type GraphEdge = {
  id: string;
  source: string;
  target: string;
  type: string;
  label?: string | null;
  properties: Record<string, unknown>;
};

export type InvestigationGraph = {
  nodes: GraphNode[];
  edges: GraphEdge[];
};
