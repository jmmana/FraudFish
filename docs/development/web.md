# Web App

## Start

```bash
cd apps/web
npm install
cp .env.example .env
npm run dev
```

The web app expects the API at `http://localhost:8000` by default.

The first analyst dashboard includes:
- case summary
- agent activity cards
- case assessment
- investigation relationship graph
- node inspector

The graph currently uses fictional demo data and will become case-specific when persistent graph storage is connected.
