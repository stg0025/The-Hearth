# The Hearth

The Hearth is a psychology-informed behavioral addiction tool.
It helps users identify what they are feeling and what unmet needs they may be medicating through compulsive behavior.
The approach is trauma-informed and focuses on unmet needs rather than surface level behavior.

## Psychology Frameworks

- **Cowen & Keltner's 27-category emotion taxonomy** — an empirically validated model of human emotion used for daily check-ins
- **ACT Urge Surfing** — an Acceptance and Commitment Therapy technique for riding out cravings without acting on them
- **NVC Needs Inventory** — Marshall Rosenberg's Nonviolent Communication framework used to identify unmet psychological needs underlying compulsive behavior

## Features

- Daily emotion and needs check-in based on Cowen & Keltner's 27 emotions
- Total day log
- Urge surfing assistant with real-time 5-minute interval tracking
- Relapse logging
- React web frontend
- CLI interface

## Tech Stack

**Backend:** Python 3.10+, FastAPI, SQLite, bcrypt, PyJWT, python-dotenv  
**Frontend:** React (Vite), Recharts, Axios

## Security

- **Bcrypt Hashing:** Password hashing with unique salt per user; plaintext passwords are never stored or transmitted.
- **Injection Prevention:** SQL injection protection via `?` placeholders on all SQLite queries.
- **JWT Authentication:** Token-based authentication with 24hr expiry and `SECRET_KEY` environment isolation.
- **Protected Endpoints:** Strict Bearer token requirements for `/checkin`, `/craving`, and `/dashboard`.
- **Local Storage:** Current version stores data in a local SQLite instance with no network exposure.
---

## Prerequisites

- Python 3.10+
- Node.js 18+ — https://nodejs.org

---

## Installation

### Backend

```bash
cd hearth-backend
pip install fastapi uvicorn bcrypt PyJWT python-dotenv rich matplotlib pandas
```

Initialize the database (first time only):

```bash
python db.py
```

Create a `.env` file inside `hearth-backend/`:

```
SECRET_KEY=your-secret-key-here
```

### Frontend

```bash
cd hearth-frontend
npm install
```

---

## Running the App

### Web (React frontend + FastAPI backend)

Open two terminals.

**Terminal 1 — backend:**

```bash
cd hearth-backend
python -m uvicorn api:app --reload
```

Backend runs at `http://127.0.0.1:8000`

**Terminal 2 — frontend:**

```bash
cd hearth-frontend
npm run dev
```

Frontend runs at `http://localhost:5173`

Open `http://localhost:5173` in your browser. The frontend proxies all API calls to the backend automatically — no CORS configuration needed.

### CLI (no frontend required)

```bash
cd hearth-backend
python main.py
```

---

## API Endpoints

| Method | Endpoint | Auth required | Description |
|--------|----------|---------------|-------------|
| POST | `/register` | No | Create account |
| POST | `/login` | No | Login, returns JWT token |
| POST | `/checkin` | Yes | Submit daily check-in |
| POST | `/craving` | Yes | Log urge surfing session |
| GET | `/dashboard` | Yes | Fetch days tracked and session history |

Interactive API docs available at `http://127.0.0.1:8000/docs` when the backend is running.

---

## Project Structure

```
The-Hearth/
├── hearth-backend/
│   ├── api.py           FastAPI app and route definitions
│   ├── auth.py          Registration and login logic
│   ├── auth_token.py    JWT creation and verification
│   ├── constants.py     Emotions and needs lists
│   ├── db.py            Database setup and queries
│   ├── display.py       CLI display helpers
│   ├── export.py        CSV export
│   ├── main.py          CLI entry point
│   ├── sessions.py      Session logic
│   ├── .env             SECRET_KEY (create this, do not commit)
│   └── cravify.db       SQLite database (auto-created)
│
└── hearth-frontend/
    ├── src/
    │   ├── api/         Axios client and endpoint calls
    │   ├── components/  Layout, ProtectedRoute, Safety prompt
    │   ├── context/     AuthContext — token and user state
    │   ├── pages/       AuthPage, DashboardPage, CheckinPage, CravingPage
    │   └── styles/      Global CSS variables and base reset
    ├── vite.config.js   Dev proxy config
    └── package.json
```

---


## Important Note

This tool is not a diagnostic instrument and does not provide professional mental health treatment.
It is intended to support mindfulness around personal needs and emotional patterns only.
It is scoped to behavioral addictions with no physical withdrawal risk.

If you are experiencing a mental health crisis or thoughts of self-harm, call or text **988** (US).
