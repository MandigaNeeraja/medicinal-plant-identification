# New App Setup (React + REST API)

## Architecture

| Component | Folder | Port |
|-----------|--------|------|
| Backend API | `backend/` | 5001 |
| React frontend | `frontend/` | 5173 |
| Legacy webapp | `webapp/` (deprecated) | 5000 |

## Prerequisites

- Python 3.12 (TensorFlow does not support Python 3.14 yet)
- Node.js 18+

## Setup

```bash
# 1. Environment
copy .env.example .env
# Edit .env — add SECRET_KEY, JWT_SECRET_KEY, GROQ_API_KEY
# Optional: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET for Google sign-in

# 2. Python dependencies
py -3.12 -m pip install -r requirements.txt

# 3. Frontend dependencies
cd frontend
npm install
```

## Run

**Terminal 1 — Backend:**
```bash
py -3.12 backend/run.py
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Open **http://localhost:5173**

## Features

- JWT authentication (access + refresh cookies)
- Email/password register & login
- Google OAuth (when configured in `.env`)
- Plant identification with CNN model
- AI chat assistant (Groq)
- Prediction history & profile page

## API Endpoints

| Route | Description |
|-------|-------------|
| `POST /api/auth/register` | Create account |
| `POST /api/auth/login` | Sign in |
| `POST /api/auth/logout` | Sign out |
| `POST /api/auth/refresh` | Refresh access token |
| `GET /api/auth/me` | Current user |
| `GET /api/plants` | List plants |
| `POST /api/predictions/predict` | Upload & predict |
| `GET /api/predictions/history` | User history |
| `POST /api/chat/init` | Start plant chat |
| `POST /api/chat/message` | Send chat message |

## Backend structure

```
backend/app/
├── __init__.py       # create_app() factory
├── config.py         # env-based configuration
├── extensions.py     # db, jwt, bcrypt, cors
├── models/           # User, Prediction, ChatSession, ChatMessage
├── api/              # REST blueprints
└── services/         # business logic
```

## Notes

- Do not run the legacy `webapp/app.py` at the same time if port 5000 is in use
- The new API defaults to port **5001** to avoid conflicts
- SQLite database is created at `instance/app.db`
- Uploads are stored in `uploads/{user_id}/`
