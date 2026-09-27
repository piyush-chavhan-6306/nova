# Dogfood Hackathon Portal — Full Backend Implementation Plan

## 0. Final Stack

Use:

```text
Backend
├── Python
├── FastAPI
├── SQLAlchemy 2.x
├── Pydantic v2
├── PostgreSQL
├── Alembic
├── pytest
└── Uvicorn

Infrastructure
├── Docker
├── Docker Compose
└── .env configuration

Optional integrations
├── Payment gateway
├── Email service
└── Object/file storage
```

### Don't add yet

```text
❌ Kubernetes
❌ Redis
❌ Celery
❌ Microservices
❌ GraphQL
❌ Kafka
```

We want a **modular monolith**.

That's much easier to build and maintain during a 72-hour hackathon.

---

# 1. Backend Architecture

This is the structure Antigravity should implement:

```text
Frontend
   │
   │ REST / JSON
   ▼
┌─────────────────────────────┐
│         FastAPI             │
│                             │
│  Routers / API Layer        │
│           ↓                 │
│  Dependencies               │
│           ↓                 │
│  Services / Business Logic  │
│           ↓                 │
│  Repositories               │
│           ↓                 │
│  SQLAlchemy Models          │
└──────────────┬──────────────┘
               │
               ▼
        PostgreSQL
```

Supporting systems:

```text
FastAPI
 ├── Authentication / Authorization
 ├── Validation
 ├── Audit logging
 ├── Error handling
 ├── OpenAPI documentation
 └── API versioning

PostgreSQL
 ├── Users
 ├── Hackathons
 ├── Teams
 ├── Submissions
 ├── Judges
 ├── Judging
 ├── Results
 └── Payments
```

---

# 2. Project Structure

Tell Antigravity to create:

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   └── exceptions.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── hackathon.py
│   │   ├── track.py
│   │   ├── team.py
│   │   ├── team_member.py
│   │   ├── team_invitation.py
│   │   ├── submission.py
│   │   ├── submission_check.py
│   │   ├── judge.py
│   │   ├── judge_track.py
│   │   ├── judge_assignment.py
│   │   ├── rubric.py
│   │   ├── rubric_criterion.py
│   │   ├── review.py
│   │   ├── score.py
│   │   ├── result.py
│   │   ├── registration.py
│   │   ├── payment.py
│   │   └── audit_log.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── hackathon.py
│   │   ├── track.py
│   │   ├── team.py
│   │   ├── submission.py
│   │   ├── judge.py
│   │   ├── assignment.py
│   │   ├── rubric.py
│   │   ├── review.py
│   │   ├── result.py
│   │   ├── registration.py
│   │   └── payment.py
│   │
│   ├── routers/
│   │   ├── users.py
│   │   ├── hackathons.py
│   │   ├── tracks.py
│   │   ├── teams.py
│   │   ├── submissions.py
│   │   ├── gallery.py
│   │   ├── judges.py
│   │   ├── assignments.py
│   │   ├── rubrics.py
│   │   ├── reviews.py
│   │   ├── results.py
│   │   ├── registrations.py
│   │   ├── payments.py
│   │   └── audit_logs.py
│   │
│   ├── services/
│   │   ├── hackathon_service.py
│   │   ├── team_service.py
│   │   ├── submission_service.py
│   │   ├── validation_service.py
│   │   ├── judge_service.py
│   │   ├── assignment_service.py
│   │   ├── judging_service.py
│   │   ├── result_service.py
│   │   ├── registration_service.py
│   │   ├── payment_service.py
│   │   └── audit_service.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── hackathon_repository.py
│   │   ├── team_repository.py
│   │   ├── submission_repository.py
│   │   ├── judge_repository.py
│   │   ├── review_repository.py
│   │   └── result_repository.py
│   │
│   └── utils/
│       ├── enums.py
│       ├── pagination.py
│       └── validators.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── acceptance/
│
├── scripts/
│   ├── seed_fixtures.py
│   └── reset_database.py
│
├── alembic/
│
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

# 3. Database Implementation

Implement the schema we finalized.

### Core

```text
users
hackathons
tracks
teams
team_members
team_invitations
submissions
submission_checks
```

### Judging

```text
judges
judge_tracks
judge_assignments
rubrics
rubric_criteria
reviews
scores
results
```

### Registration / Payment

```text
registrations
payments
```

### System

```text
audit_logs
```

---

# 4. Database Rules

Antigravity should **not blindly convert JSON into tables**.

`fixtures.json` is input data.

The database should be normalized.

For example:

```text
Fixture

judge:
{
  id,
  name,
  email,
  tracks: [...]
}
```

becomes:

```text
users
   ↓
judge
   ↓
judge_tracks
   ↓
tracks
```

Likewise:

```text
scores
{
   judge,
   project,
   criteria,
   comment
}
```

should become proper judging relationships.

---

# 5. Alembic

Use migrations from the beginning.

```text
alembic/
   ↓
migration 001
   ↓
migration 002
   ↓
migration 003
```

Commands should work:

```bash
alembic upgrade head
```

and:

```bash
alembic downgrade -1
```

Never make Antigravity rely on manually creating database tables.

---

# 6. Fixture Seeding

This is extremely important.

Create:

```text
scripts/seed_fixtures.py
```

Flow:

```text
fixtures.json
      ↓
Parse JSON
      ↓
Validate
      ↓
Transform
      ↓
Insert/update
      ↓
PostgreSQL
```

It should be **idempotent**.

Meaning:

```bash
python scripts/seed_fixtures.py
```

multiple times should not create duplicate records.

Use fixture IDs where appropriate so that:

```text
evt_...
trk_...
jdg_...
tm_...
prj_...
```

remain traceable to the original fixture data.

---

# 7. API Implementation Order

This is important.

Don't let Antigravity build routes randomly.

### Phase A — Foundation

```text
/config
/database
/error handling
/dependencies
/models
/migrations
```

Then:

### Phase B — Users + Events

```text
/users
/hackathons
/tracks
```

Then:

### Phase C — Teams

```text
/teams
/team-invitations
```

Then:

### Phase D — Submissions

```text
/submissions
/submission checks
/gallery
```

Then:

### Phase E — Judging

```text
/judges
/judge-tracks
/judge-assignments
```

Then:

### Phase F — Scoring

```text
/rubrics
/reviews
/scores
```

Then:

### Phase G — Results

```text
/results
/export
```

Then:

### Phase H — Registration / Payment

```text
/registrations
/payments
```

Then:

### Phase I — Audit

```text
/audit-logs
```

---

# 8. API Contract

This is especially important because **you're building frontend later**.

Every endpoint needs:

```text
Method
Route
Authentication requirement
Role requirement
Request schema
Response schema
Validation rules
Error responses
```

For example:

```text
POST /submissions
```

### Request

```json
{
  "team_id": "tm_01",
  "track_id": "trk_01",
  "title": "My Project",
  "summary": "Project summary",
  "repo_url": "https://github.com/...",
  "demo_url": "https://..."
}
```

### Response

```json
{
  "id": "prj_01",
  "status": "DRAFT",
  "title": "My Project",
  "track_id": "trk_01",
  "created_at": "..."
}
```

The frontend developer then knows **exactly what to send and what to expect.**

---

# 9. Authorization

This should be centralized.

Don't write authorization separately in every route.

Create something like:

```text
dependencies.py
```

with reusable checks:

```text
require_participant()
require_judge()
require_organizer()
require_admin()
require_team_member()
require_team_lead()
require_assigned_judge()
```

Example:

```text
Judge
 ↓
GET /reviews/{id}
 ↓
Is user a judge?
 ↓
Is this review assigned to this judge?
 ↓
YES → return
NO → 403
```

This is critical for the judging system.

---

# 10. Submission Business Logic

Create:

```text
submission_service.py
```

It should handle:

```text
Create draft
     ↓
Edit draft
     ↓
Validate
     ↓
Submit
     ↓
Lock
```

Submission cannot be finalized if:

```text
event closed
team invalid
missing required fields
invalid track
duplicate submission
already locked
```

---

# 11. Judging Business Logic

Create:

```text
judging_service.py
```

Flow:

```text
Judge assignment
       ↓
Judge opens project
       ↓
Create review
       ↓
Score criteria
       ↓
Calculate weighted score
       ↓
Submit review
       ↓
Lock review
```

Example:

```text
Functionality     4/5 × 40%
Quality           5/5 × 30%
Innovation        4/5 × 30%
                   ↓
              Final score
```

Keep the calculation in the backend.

---

# 12. Results Service

Create:

```text
result_service.py
```

Initially:

```text
Reviews
   ↓
Scores
   ↓
Weighted average
   ↓
Raw result
   ↓
Results table
```

Later T3/T4 can plug into this:

```text
Raw scores
    ↓
Normalization
    ↓
Outlier handling
    ↓
Advanced judging
    ↓
Final results
```

So we're deliberately leaving an extension point here.

---

# 13. Gallery

The frontend should **not construct project data itself**.

Backend should return something like:

```json
{
  "id": "prj_01",
  "title": "Project X",
  "summary": "...",
  "team": {
    "id": "tm_01",
    "name": "Team Raptors"
  },
  "track": {
    "id": "trk_01",
    "name": "AI"
  },
  "repo_url": "...",
  "demo_url": "..."
}
```

That will make your Stitch frontend much easier to connect later.

---

# 14. Pagination / Search / Filtering

Build these into list APIs from the beginning.

For example:

```text
GET /gallery?page=1&page_size=20
```

and:

```text
GET /gallery?track_id=trk_01
```

and:

```text
GET /gallery?search=health
```

Likewise:

```text
GET /hackathons/{id}/submissions
```

should support filtering.

This will make the Stitch gallery and organizer dashboards much easier.

---

# 15. Standard API Responses

Use consistent error responses.

Example:

```json
{
  "detail": "Submission deadline has passed"
}
```

HTTP codes:

```text
200 → Success
201 → Created
204 → Deleted
400 → Bad request
401 → Unauthenticated
403 → Not allowed
404 → Not found
409 → Conflict
422 → Validation error
500 → Server error
```

Don't return random formats from different endpoints.

---

# 16. OpenAPI Documentation

FastAPI automatically provides:

```text
/docs
/redoc
/openapi.json
```

Make sure every endpoint has:

- summary
- description
- request schema
- response schema
- possible errors
- tags

This becomes extremely useful when you start frontend.

Your frontend developer can literally open:

```text
/docs
```

and understand the API.

---

# 17. CORS

Since frontend and backend may run separately:

```text
Frontend
http://localhost:3000

Backend
http://localhost:8000
```

configure CORS properly.

Do **not** permanently use:

```text
allow_origins=["*"]
```

for production.

Use environment configuration.

---

# 18. Docker

Eventually:

```text
docker compose up
```

should start:

```text
┌──────────────────────┐
│ Frontend             │
│ React / Next.js      │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│ FastAPI              │
│ Port 8000            │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│ PostgreSQL            │
│ Port 5432             │
└──────────────────────┘
```

And startup should perform:

```text
Postgres starts
     ↓
health check
     ↓
Alembic migration
     ↓
fixture seed
     ↓
FastAPI starts
```

This is important for your final evaluation.

---

# 19. Environment Configuration

Create:

```text
.env.example
```

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/dogfood

APP_ENV=development
SECRET_KEY=change-me

PAYMENT_REQUIRED=false
PAYMENT_PROVIDER=
PAYMENT_API_KEY=

FRONTEND_URL=http://localhost:3000
```

Never commit:

```text
.env
```

---

# 20. Testing Strategy

Don't wait until the end to test.

### Unit tests

Test:

```text
deadline calculation
team size validation
score calculation
event status
payment status
```

### Integration tests

Test:

```text
API → Service → PostgreSQL
```

### Acceptance tests

Specifically test:

```text
public gallery
fixture project visibility
closed submission rejection
judge own scores
judge peer score isolation
participant score isolation
organizer CSV export
```

---

# 21. Fixture Edge Cases

Antigravity must **not simplify away awkward fixture data**.

The official fixture intentionally contains cases such as:

```text
judge with same score pattern
incomplete review batches
duplicate submission
different review counts
missing score entries
```

The backend should handle these without crashing.

This is one of the reasons we're using proper relational models rather than assuming:

```text
every project = same number of reviews
```

---

# 22. Payment Module

Keep it isolated.

```text
registration_service
        ↓
payment_service
        ↓
payment provider
```

If:

```text
payment_required = false
```

then:

```text
Registration → confirmed
```

If:

```text
payment_required = true
```

then:

```text
Registration
      ↓
Payment
      ↓
SUCCESS
      ↓
Confirmed
```

Don't hard-code Razorpay/Stripe/etc. throughout the application.

Create a provider abstraction so the actual provider can be plugged in later.

---

# 23. Audit System

Important actions automatically create:

```text
audit_logs
```

Examples:

```text
HACKATHON_CREATED
TEAM_CREATED
SUBMISSION_CREATED
SUBMISSION_SUBMITTED
SUBMISSION_LOCKED
JUDGE_ASSIGNED
REVIEW_STARTED
SCORE_SUBMITTED
RESULT_PUBLISHED
PAYMENT_COMPLETED
```

This will also help when explaining your architecture during judging.

---

# 24. T3/T4 Extension Strategy

Don't implement T3/T4 now.

But design extension points:

```text
services/
├── judging_service.py
├── result_service.py
└── normalization_service.py   ← later
```

Later:

```text
T3
├── normalization
├── advanced assignments
├── advanced analytics
└── additional judging modes

T4
├── advanced workflows
├── advanced integrations
└── additional platform capabilities
```

The core API shouldn't need to be destroyed.

---

# 25. What Antigravity Should NOT Do

This is very important.

Tell it:

```text
Do not:
- invent unnecessary features
- create microservices
- add Kubernetes
- add Redis without a requirement
- add GraphQL
- hardcode fixture data inside models
- couple business logic directly to routers
- expose SQLAlchemy models directly as API responses
- put authorization only in the frontend
- hardcode payment provider logic
- create duplicate database structures
- remove awkward fixture edge cases
- build frontend components inside the backend
```

---

# 26. Definition of "Backend Complete"

Before you move to frontend, you should be able to say:

```text
✅ PostgreSQL schema works
✅ Alembic migrations work
✅ fixtures.json seeds correctly
✅ FastAPI starts
✅ Swagger works
✅ All core routes work
✅ Authorization works
✅ Team workflow works
✅ Submission workflow works
✅ Gallery works
✅ Judge assignment works
✅ Review/scoring works
✅ Results work
✅ CSV export works
✅ Optional registration/payment architecture works
✅ Audit logs work
✅ Tests pass
✅ Docker Compose works
✅ Frontend can consume APIs
```

---

# 27. Most Important: How You'll Work With Antigravity

Don't give Antigravity this entire thing and say:

> "Build everything."

That can create a messy codebase.

Instead, work **phase by phase**.

### Prompt 1

```text
Implement Phase 1: backend foundation.

Create the FastAPI project structure, configuration,
PostgreSQL connection, SQLAlchemy 2.x setup, Pydantic v2,
Alembic migrations, centralized error handling,
dependency injection, and Docker configuration.

Do not implement business features yet.

Keep the architecture modular and suitable for future
T1/T2/T3/T4 expansion.

Do not add unnecessary technologies.
```

Then test.

### Prompt 2

```text
Now implement the finalized database models and Alembic
migration according to DATA-MODEL.md.

Do not invent additional tables or relationships.
Preserve the existing architecture.

Then create the fixture seeding system for fixtures.json.
The seed process must be idempotent.
```

Then test.

### Prompt 3

```text
Now implement Hackathons, Tracks, Users and Teams,
including their schemas, repositories, services and routers.

Follow the API contract.
Implement authorization and validation in the backend.
Add unit and integration tests.
Do not modify unrelated modules.
```

Then continue:

```text
Submissions
↓
Judges
↓
Assignments
↓
Rubrics
↓
Reviews
↓
Scores
↓
Results
↓
CSV
↓
Registration/Payment
↓
Audit
```

---

# 28. Frontend Integration Goal

When you eventually open your Stitch frontend project, you shouldn't be thinking:

> "How do I connect this?"

You should already have:

```text
GET /gallery
GET /hackathons/{id}
GET /teams/{id}
GET /submissions/{id}
GET /judges/me/assignments
GET /judges/me/reviews
GET /hackathons/{id}/results
```

and so on.

So the frontend becomes:

```text
Stitch UI
    ↓
API client
    ↓
FastAPI
    ↓
PostgreSQL
```

rather than changing backend architecture while you're simultaneously designing the UI.

---

# 29. Backend Build Order

```text
                 BACKEND
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
     FOUNDATION            DATABASE
          │                   │
          └─────────┬─────────┘
                    ↓
              FIXTURE SEED
                    ↓
              USERS / EVENTS
                    ↓
                  TEAMS
                    ↓
              SUBMISSIONS
                    ↓
               GALLERY
                    ↓
          JUDGES / ASSIGNMENTS
                    ↓
            RUBRICS / REVIEWS
                    ↓
               SCORES
                    ↓
              RESULTS / CSV
                    ↓
          REGISTRATION / PAYMENT
                    ↓
               AUDIT LOG
                    ↓
              TEST EVERYTHING
                    ↓
             DOCKER COMPOSE
                    ↓
             ┌──────────────┐
             │   FRONTEND   │
             │    STITCH    │
             └──────────────┘
```

**This is the plan I'd use for your backend.** The key is that we're not building a throwaway "acceptance-test backend"; we're building the actual Hackathon Portal foundation, with the official Dogfood checks acting as our verification layer.
