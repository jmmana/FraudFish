# Local Development Quickstart

## Prerequisites

- Docker + Docker Compose
- Python 3.12+

## Start infrastructure

```bash
docker compose up -d
docker compose ps
```

Expected local services:

- PostgreSQL: `localhost:5432`
- Neo4j Browser: `http://localhost:7474`
- Neo4j Bolt: `localhost:7687`
- Redis: `localhost:6379`

## Start API

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

Then open:

- API health: `http://localhost:8000/health`
- OpenAPI docs: `http://localhost:8000/docs`

## Safety

The MVP must use fictional data only. Do not place production customer PII, bank credentials, sanctions-provider credentials or API keys in the repository.
