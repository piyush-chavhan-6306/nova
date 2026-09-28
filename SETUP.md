# 🚀 NOVA – Hackathon Portal Platform: Setup Guide

Complete instructions for configuring, running, testing, and deploying the **NOVA Hackathon Portal** platform using Docker or native execution environments.

---

## 📋 Prerequisites

- **Docker & Docker Compose** (Recommended)
- **Python 3.11+**
- **Node.js 18+ & npm** (if running frontend locally)
- **PostgreSQL 15+** (if running database outside Docker)

---

## ⚙️ Environment Configuration

Create a `.env` file in the `backend` directory or repository root:

```env
# Database Settings (Local Docker PostgreSQL)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=nova_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@db:5432/nova_db

# Backend Configuration
BACKEND_PORT=8000
PROJECT_NAME="NOVA Hackathon Portal API"
VERSION="1.0.0"
ENVIRONMENT="development"
DEBUG=True
SECRET_KEY="nova-dev-secret-key-change-in-production-12345"
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:8000"]

# Frontend Configuration
FRONTEND_PORT=3000
VITE_API_URL=http://localhost:8000
```

---

## 🏃 Running the Application

### Option 1: Using Docker Compose (Recommended)

Start all services (PostgreSQL database, Backend FastAPI API):

```bash
cd backend
docker compose up -d --build
```

To view live logs:
```bash
docker compose logs -f
```

To stop all containerized services:
```bash
docker compose down
```

To seed initial database fixtures inside Docker:
```bash
docker compose exec api python scripts/seed_fixtures.py
```

---

### Option 2: Native Execution (Windows PowerShell / CMD / Linux / macOS)

#### Terminal 1 — Start Backend Service:
```bash
cd backend
pip install -r requirements.txt
python scripts/seed_fixtures.py
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2 — Start Frontend Application (if applicable):
```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Application Access Points

| Service | URL | Description |
| :--- | :--- | :--- |
| **Backend REST API** | `http://localhost:8000` | FastAPI root endpoint |
| **Health Check** | `http://localhost:8000/health` | System & DB connectivity health check |
| **API Documentation** | `http://localhost:8000/docs` | Interactive Swagger UI (83 API Endpoints) |
| **ReDoc Documentation** | `http://localhost:8000/redoc` | OpenAPI Schema documentation |

---

## 👤 Default Demo Roles

1. **Admin Portal**:
   - Email: `admin@nova.dev`
   - Role Header / Auth: `usr_admin_001`

2. **Organizer Portal**:
   - Email: `organizer@nova.dev`
   - Role Header / Auth: `usr_org_001`

3. **Judge Portal**:
   - Email: `judge@nova.dev`
   - Role Header / Auth: `usr_judge_001`

4. **Participant Portal**:
   - Email: `participant@nova.dev`
   - Role Header / Auth: `usr_participant_001`

---

## 🧪 Running Automated Tests

Execute the complete backend unit test suite (37 unit tests covering T1–T4 features):
```bash
cd backend
pytest tests/unit/ -v
```

Execute database fixture seeding verification:
```bash
cd backend
python scripts/check_db.py
```
