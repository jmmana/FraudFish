from fastapi import FastAPI

app = FastAPI(
    title="FraudFish API",
    version="0.1.0",
    description="Multi-agent fraud and financial-crime investigation API.",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "fraudfish-api"}
