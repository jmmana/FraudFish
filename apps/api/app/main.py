from fastapi import FastAPI

from app.api.cases import router as cases_router
from app.api.demo import router as demo_router
from app.api.investigations import router as investigations_router


app = FastAPI(
    title="FraudFish API",
    version="0.3.0",
    description="Multi-agent fraud and financial-crime investigation API.",
)

app.include_router(cases_router)
app.include_router(investigations_router)
app.include_router(demo_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "fraudfish-api"}
