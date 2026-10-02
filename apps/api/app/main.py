from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.cases import router as cases_router
from app.api.demo import router as demo_router
from app.api.graph import router as graph_router
from app.api.investigations import router as investigations_router


app = FastAPI(
    title="FraudFish API",
    version="0.4.1",
    description="Multi-agent fraud and financial-crime investigation API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(cases_router)
app.include_router(investigations_router)
app.include_router(demo_router)
app.include_router(graph_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "fraudfish-api"}
