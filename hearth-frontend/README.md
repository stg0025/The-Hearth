# The Hearth — Frontend

React (Vite) frontend for The Hearth FastAPI backend.

## Prerequisites

- Node.js 18+  (https://nodejs.org)
- The Hearth backend running on port 8000

## Install

```bash
cd hearth-frontend
npm install
```

## Run (dev)

Start the FastAPI backend first:

```bash
# from repo root
python -m uvicorn api:app --reload
```

Then in a separate terminal start the frontend:

```bash
npm run dev
```

Visit http://localhost:5173

The Vite dev server proxies all `/api/*` requests to `http://127.0.0.1:8000`,
so no CORS config is needed during development.

## Build (production)

```bash
npm run build
# output in dist/
```

Serve `dist/` with any static file host or reverse-proxy it behind the FastAPI
server with a `StaticFiles` mount (see FastAPI docs).

## Project structure

```
src/
  api/         axios client + all endpoint calls
  components/  Layout, ProtectedRoute
  context/     AuthContext (token + user state)
  pages/       AuthPage, DashboardPage, CheckinPage, CravingPage
  styles/      global.css (CSS variables, base reset)
  App.jsx      router
  main.jsx     entry
```

## Next steps (per roadmap)

- Migrate to Next.js (App Router) for SSR
- PostgreSQL migration — update api/client.js base URL to point at new host
- ML relapse prediction — add a `/predict` endpoint call and surface results on Dashboard
