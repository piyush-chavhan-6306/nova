# 🚀 NOVA — Hackathon Management & Judging Platform (`dogfood-NOVA`)

NOVA is a modular monolith backend implementation built for the **DOGFOOD 2026** hackathon portal specification. It supports full hackathon lifecycle administration, multi-criteria scoring rubrics, algorithmic judge workload balancing, pairwise head-to-head project evaluation, judge calibration, blind review, outlier score detection, conflict of interest recusal workflows, and result state machines.

---

## 🏗️ Project Architecture & Tech Stack

- **Project Name**: NOVA Hackathon Portal (`dogfood-NOVA`)
- **Backend Framework**: FastAPI (Python 3.12)
- **Frontend Framework**: React 18, Vite, TypeScript
- **Database Engine**: PostgreSQL 15+ (SQLAlchemy ORM + `psycopg2-binary`)
- **API Protocol**: RESTful API under `/api/v1` namespace (83 Endpoints)
- **Containerization**: Docker & Docker Compose (`docker compose up --build`)
- **Testing & Verification**: 37 Pytest unit tests + DOGFOOD acceptance checker (`run.py`)

---

## 🎯 Verification Status (T1–T4 Verified)

```text
DOGFOOD 2026 acceptance report
portal: http://localhost:8000
claimed: T1 T2 T3 T4
fixtures: dogfood-portal/dogfood/fixtures (1).json

T1  gallery is public ...................... PASS
T1  project from fixtures shown ............ PASS
T1  closed event refuses submissions ....... PASS
T2  judge sees own scores .................. PASS
T2  judge cannot see peer scores ........... PASS
T2  participant blocked .................... PASS
T2  csv export works ....................... PASS
T3  pairwise & calibration statistics API .. PASS
T4  audit trail & integrity analytics API .. PASS

claimed T1 T2 T3 T4, verified T1 T2 T3 T4
```

---

## 🚀 Quick Start & Installation

### Option 1: Docker Compose (Recommended)
This runs the complete stack: Frontend (Vite), Backend (FastAPI), and Database (Postgres).
```bash
docker compose up --build
```
- Frontend UI: http://localhost:5173
- Backend API Docs: http://localhost:8000/docs

### Option 2: Local Development
**Backend Setup**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

---

## 📄 Key System Documentation
- [SETUP.md](SETUP.md): Detailed installation, configuration, & environment guide
- [ARCHITECTURE.md](ARCHITECTURE.md): System design, modular monolith pattern, & security guards
- [DATA-MODEL.md](DATA-MODEL.md): PostgreSQL schema & entity relationships
- [JUDGING.md](JUDGING.md): Rubrics, Pairwise, Calibration, Outliers, & State Machine specs
- [INTEGRATION_GAPS.md](INTEGRATION_GAPS.md): Missing API details to support UI
- [HACKATHON_CONTENT_GAPS.md](HACKATHON_CONTENT_GAPS.md): Documented frontend UI features that are pending backend support