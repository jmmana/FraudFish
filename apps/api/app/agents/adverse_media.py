from __future__ import annotations

from app.agents.contracts import AgentContext, AgentResult, AgentStatus
from app.connectors.news import DemoNewsConnector, NewsConnector


ADVERSE_TERMS = (
    "fraud",
    "money laundering",
    "corruption",
    "sanctions",
    "arrest",
    "arrested",
    "investigation",
    "scam",
)


class AdverseMediaAgent:
    name = "adverse_media"

    def __init__(self, connector: NewsConnector | None = None) -> None:
        self.connector = connector or DemoNewsConnector()

    def run(self, context: AgentContext) -> AgentResult:
        subject_name = str(context.inputs.get("subject_name") or "").strip()
        if not subject_name:
            return AgentResult(
                agent=self.name,
                status=AgentStatus.SUCCEEDED,
                summary="Adverse-media search skipped because no subject name was provided.",
                metadata={"screened": False},
            )

        articles = self.connector.search(subject_name)
        signals = []
        evidence = []

        for article in articles:
            title_lower = article.title.lower()
            adverse_terms = [term for term in ADVERSE_TERMS if term in title_lower]

            evidence.append(
                {
                    "source_type": "news",
                    "source_ref": article.url,
                    "reliability": "medium",
                    "payload": {
                        "title": article.title,
                        "domain": article.source_domain,
                        "published_at": article.published_at,
                        "language": article.language,
                        "tone": article.tone,
                        "adverse_terms": adverse_terms,
                    },
                }
            )

            if adverse_terms:
                signals.append(
                    {
                        "signal_type": "adverse_media_candidate",
                        "severity": "medium",
                        "summary": (
                            "Potential adverse-media article found; identity and allegation "
                            "require independent human verification."
                        ),
                    }
                )

        return AgentResult(
            agent=self.name,
            status=AgentStatus.SUCCEEDED,
            summary=f"Reviewed {len(articles)} news article candidate(s).",
            signals=signals,
            evidence=evidence,
            findings=(
                [
                    {
                        "statement": (
                            f"{len(signals)} potential adverse-media candidate(s) found. "
                            "No article alone confirms identity or wrongdoing."
                        ),
                        "confidence": 0.5,
                    }
                ]
                if signals
                else []
            ),
            metadata={
                "screened": True,
                "article_count": len(articles),
                "candidate_count": len(signals),
                "identity_confirmed": False,
                "human_validation_required": True,
            },
        )
