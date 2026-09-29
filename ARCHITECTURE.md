# 🏛️ ARCHITECTURE.md — System Architecture & Design Rationale

## 1. Overview
The **NOVA Hackathon Portal** is designed as a fully integrated **React/Vite Frontend** backed by a **FastAPI Modular Monolith** (Python 3.12) and **PostgreSQL**. It provides full compliance with the DOGFOOD 2026 specification, supporting end-to-end hackathon lifecycle management, multi-criteria scoring rubrics, pairwise evaluation, judge calibration, peer isolation, conflict recusal workflows, and result state machines.

---

## 2. Architectural Layers

```
                                ┌───────────────────────────┐
                                │    React Frontend UI      │
                                │    (Vite, TypeScript)     │
                                └─────────────┬─────────────┘
                                              │ HTTP / REST
                                              ▼
                               ┌───────────────────────────┐
                               │      FastAPI Routers      │
                               │  (RBAC & Auth Middleware) │
                               └─────────────┬─────────────┘
                                             │
                                             ▼
                               ┌───────────────────────────┐
                               │     Domain Services       │
                               │ (Business & Scoring Logic)│
                               └─────────────┬─────────────┘
                                             │
                                             ▼
                               ┌───────────────────────────┐
                               │   Repositories Layer      │
                               │  (Encapsulated Queries)   │
                               └─────────────┬─────────────┘
                                             │
                                             ▼
                               ┌───────────────────────────┐
                               │  PostgreSQL / SQLAlchemy  │
                               │     (Relational DB)       │
                               └───────────────────────────┘
```

### Layer Responsibilities
1. **Routers (`app/routers/`)**: Endpoint definitions handling HTTP serialization, response status codes, and input dependency injection.
2. **Services (`app/services/`)**: Core domain engine encapsulating business workflows, scoring computations, conflict checking, and state transitions.
3. **Repositories (`app/repositories/`)**: Encapsulated database queries separating data access from business rules.
4. **Models (`app/models/`)**: SQLAlchemy declarative ORM data models.
5. **Schemas (`app/schemas/`)**: Pydantic v2 data validation schemas.

---

## 3. Key Design Decisions

### 🔒 Backend Peer Isolation Guard
Judge privacy and peer isolation are strictly enforced at the database/backend layer. When a judge requests evaluation details (`/api/v1/judges/{id}/assignments`), the backend verifies the caller identity (`UserIdentity`). If a judge attempts to access another judge's assignments or scores, a `403 Forbidden` response is returned immediately.

### 🔄 Result State Machine (`Hackathon.results_status`)
Leaderboard results follow a strict finite state machine:
`DRAFT` ➔ `CALCULATED` ➔ `UNDER_REVIEW` ➔ `APPROVED` ➔ `PUBLISHED` ➔ `LOCKED`.
Once locked, recalculation and modifications are blocked at the service level, ensuring result immutability.

### 🛡️ Conflict of Interest & Recusal Engine
Judges can declare conflicts of interest against projects or teams. Upon declaration, active assignments for that judge are automatically revoked, and audit logs are recorded for organizer review.
