from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import httpx


@dataclass(frozen=True)
class NewsArticle:
    title: str
    url: str
    source_domain: str | None = None
    published_at: str | None = None
    language: str | None = None
    tone: float | None = None


class NewsConnector(Protocol):
    def search(self, full_name: str) -> tuple[NewsArticle, ...]:
        ...


class DemoNewsConnector:
    def search(self, full_name: str) -> tuple[NewsArticle, ...]:
        return (
            NewsArticle(
                title=f"{full_name} participates in fictional technology conference",
                url="fixture://news/neutral-001",
                source_domain="demo.example",
                published_at="2026-09-12",
                language="Spanish",
            ),
        )


class GdeltNewsConnector:
    BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

    def __init__(
        self,
        max_records: int = 50,
        timespan: str = "3months",
        timeout_seconds: float = 20.0,
    ) -> None:
        self.max_records = max(1, min(max_records, 250))
        self.timespan = timespan
        self.timeout_seconds = timeout_seconds

    def search(self, full_name: str) -> tuple[NewsArticle, ...]:
        query = (
            f'"{full_name}" '
            '(fraud OR "money laundering" OR corruption OR sanctions '
            'OR arrested OR investigation OR scam)'
        )
        response = httpx.get(
            self.BASE_URL,
            params={
                "query": query,
                "mode": "artlist",
                "format": "json",
                "maxrecords": self.max_records,
                "timespan": self.timespan,
                "sort": "datedesc",
            },
            timeout=self.timeout_seconds,
            headers={"User-Agent": "FraudFish/0.1 adverse-media"},
        )
        response.raise_for_status()
        payload = response.json()

        articles = []
        for item in payload.get("articles", []):
            title = str(item.get("title") or "").strip()
            url = str(item.get("url") or "").strip()
            if not title or not url:
                continue

            tone = item.get("tone")
            try:
                parsed_tone = float(tone) if tone is not None else None
            except (TypeError, ValueError):
                parsed_tone = None

            articles.append(
                NewsArticle(
                    title=title,
                    url=url,
                    source_domain=item.get("domain"),
                    published_at=item.get("seendate"),
                    language=item.get("language"),
                    tone=parsed_tone,
                )
            )

        return tuple(articles)
