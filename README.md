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

**Backend:** Python, FastAPI, SQLite, bcrypt, PyJWT, python-dotenv  
**Frontend:** React, Vite, Recharts, Axios

## Security

- bcrypt password hashing with unique salt per user
- Plaintext passwords are never stored or transmitted
- SQL injection prevention via `?` placeholders on all queries
- JWT authentication with 24hr expiry
- `SECRET_KEY` stored in environment variable
- Protected endpoints (`/checkin`, `/craving`, `/dashboard`) require a valid bearer token
- All data stored locally in SQLite with no network exposure in V1

---

## Prerequisites

- Python 3.10+
- Node.js 18+ — https://nodejs.org

---

## Installation

### Backend

```bash
cd Hearth-Backend
pip install fastapi uvicorn bcrypt PyJWT python-dotenv rich matplotlib pandas
```

Initialize the database (first time only):

```bash
python db.py
```

Create a `.env` file inside `Hearth-Backend/`:

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
cd Hearth-Backend
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
cd Hearth-Backend
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
├── Hearth-Backend/
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

## Roadmap

- ~~Data exporting to CSV~~ — complete
- ~~FastAPI backend~~ — complete
- ~~JWT authentication~~ — complete
- ~~React frontend~~ — complete
- Brute force lockout
- Structured audit logging
- PostgreSQL migration
- Docker containerization
- GitHub Actions CI/CD pipeline
- Next.js migration for server-side rendering
- ML relapse prediction

---

## Important Note

This tool is not a diagnostic instrument and does not provide professional mental health treatment.
It is intended to support mindfulness around personal needs and emotional patterns only.
It is scoped to behavioral addictions with no physical withdrawal risk.

If you are experiencing a mental health crisis or thoughts of self-harm, call or text **988** (US).