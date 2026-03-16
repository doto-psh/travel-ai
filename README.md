# Travel AI Chat

AI Agent chatbot application using OpenAI-compatible API.

## Quick Start

### Backend

```bash
cd backend
cp .env.example .env  # Edit with your API key
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --port 18000 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:15173

### Docker (Production-like)

```bash
cp backend/.env.example backend/.env  # Edit with your API key
docker compose up
```

### Docker (Development with hot reload)

```bash
cp backend/.env.example backend/.env  # Edit with your API key
docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up
```

## Tech Stack

- **Frontend**: SvelteKit, TypeScript, TailwindCSS v4
- **Backend**: FastAPI, SQLAlchemy 2.0 (async), SQLite
- **Auth**: JWT (python-jose + passlib/bcrypt)
