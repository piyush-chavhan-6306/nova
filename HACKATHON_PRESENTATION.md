# 🚀 NOVA Hackathon Portal — Hackathon Presentation

> **End-to-End Enterprise Hackathon Management & Fair Judging Engine**  
> **DOGFOOD 2026 Hackathon Submission** | Verified Tier 1 (Core) & Tier 2 (Judging) Compliance

---

## 📊 Presentation Overview

### Slide 1: TITLE
- **Project Name**: NOVA Hackathon Portal
- **Tagline**: The Next-Generation Enterprise Platform for Frictionless Hackathons & Unbiased Judging
- **Team**: Team NOVA Engineering
- **Hackathon**: DOGFOOD 2026 Hackathon
- **Status**: T1 (Core) COMPLETE | T2 (Judging) COMPLETE

---

### Slide 2: PROBLEM
- **Participant Pain Points**: Buggy team invites, unclear deadlines, zero feedback visibility.
- **Judge Pain Points**: Workload imbalance, track conflicts, peer score visibility, unstandardized scoring.
- **Organizer Pain Points**: Data leaks across events, manual CSV export calculation errors, lack of live auditability.

---

### Slide 3: SOLUTION
- **Integrated Solution**: High-performance, containerized web platform for full hackathon lifecycle management.
- **Main User Roles**: `ADMIN`, `ORGANIZER`, `JUDGE`, `PARTICIPANT`.
- **Core Pillars**: Enterprise RBAC, Organizer Ownership Isolation, Algorithmic Fair Judging.

---

### Slide 4: KEY FEATURES (VERIFIED)
- **Participant**: Team creation, invite links, draft/edit project before deadline, gallery search & track filters.
- **Judge**: Isolated workload dashboard, weighted rubric scoring sliders, peer isolation guards (403 on peer score access).
- **Organizer**: Dates & tracks configuration, multi-tier prize CRUD, weighted rubric builder, algorithmic batch assigner, live analytics & CSV exports.
- **Admin**: Global platform governance & system-wide analytics.

---

### Slide 5: USER WORKFLOW
- **Participant Flow**: Registration ➔ Team Creation / Join Link ➔ Draft / Edit Project ➔ Public Gallery.
- **Judge Flow**: Invite / Track Assignment ➔ Workload Inspection ➔ Multi-Criterion Rubric Evaluation ➔ Review Submission.
- **Organizer Flow**: Event Setup ➔ Rubric Builder ➔ Batch Assigner ➔ Live Analytics ➔ CSV Results Export.

---

### Slide 6: TECHNICAL ARCHITECTURE
- **Frontend**: React 18, TypeScript, Tailwind CSS, Lucide React, Vite.
- **REST API / Gateway**: FastAPI, Pydantic v2, Uvicorn.
- **Service & Repository Layer**: Modular Python services for Hackathons, Teams, Submissions, Judging, and Scoring.
- **Persistence Layer**: SQLAlchemy ORM, PostgreSQL 15, Alembic Schema Migrations.
- **Infrastructure & Security**: Docker Compose (`api`, `web`, `db`), JWT & Cookie Session Resolvers, Audit Logging.

---

### Slide 7: DATABASE / DATA MODEL
- **Major Entities**: `Hackathon`, `Track`, `Prize`, `Rubric`, `RubricCriterion`, `User`, `Team`, `TeamMember`, `Submission`, `Judge`, `JudgeTrack`, `JudgeAssignment`, `Review`, `Score`.
- **Relationships**: Hackathon 1:N Prize (Cascade Delete), Rubric 1:N RubricCriterion (Custom Weights), JudgeAssignment 1:1 Review.

---

### Slide 8: SECURITY & FAIR JUDGING
- **Authentication & RBAC**: JWT Bearer + Session Cookie resolution.
- **Organizer Ownership Isolation**: `verify_hackathon_owner` checks `organizer_id` on all event resources.
- **Judge Peer Isolation**: `require_judge_peer_isolation` blocks cross-judge score inspection (403 Forbidden).
- **Conflict Prevention**: `_validate_peer_isolation` prevents judges from evaluating their own team or competing events.
- **Cross-Judge Normalization**: Z-score calibration for fair grading.

---

### Slide 9: VERIFICATION & ENGINEERING METRICS
- **Backend Tests**: 48 Passed (0 Failed) via `pytest tests/unit/ -v`.
- **Frontend Build**: 0 Errors (`tsc -b && vite build` — 1,917 modules transformed).
- **Alembic Migration**: `18c6b51fef6f_add_prizes_table` applied cleanly.
- **Docker Setup**: Multi-container Docker Compose starts from clean state.
- **Official Acceptance Checks**: 7/7 DOGFOOD acceptance checks PASSing.
- **Tier Compliance**: T1 (Core) and T2 (Judging) fully verified.

---

### Slide 10: DEMO & CLOSING
- **Live Demo Points**: Event & Rubric setup ➔ Team submission ➔ Algorithmic batch judging ➔ Live progress & CSV export.
- **Value Proposition**: Scalable, enterprise-grade, provably fair hackathon management platform.
