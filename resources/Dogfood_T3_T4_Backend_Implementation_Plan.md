# Dogfood T3 & T4 Backend Implementation Plan

## Purpose

This document extends the existing Dogfood FastAPI + PostgreSQL backend from T1/T2 to advanced T3/T4 capabilities.

**Important:** This is an extension, not a rewrite. Existing T1/T2 functionality, routes, models, authorization, Docker setup, seed process, and tests must remain functional.

---

# 1. Non-Negotiable Rules

Antigravity must:

- Extend the existing backend; do not rewrite T1/T2.
- Do not remove or rename existing API routes.
- Do not break existing T1/T2 acceptance tests.
- Reuse the existing FastAPI modular-monolith architecture.
- Use PostgreSQL, SQLAlchemy, Pydantic, Alembic, services, repositories, and authorization dependencies already present.
- Add an Alembic migration for every database change.
- Add automated tests for every new feature.
- Run the complete existing test suite after every phase.
- Do not introduce Redis, Kafka, Celery, Kubernetes, microservices, GraphQL, or unnecessary infrastructure.

---

# 2. T3 Scope

T3 adds:

1. Advanced Judge Assignment
2. Pairwise Judging
3. Judge Calibration
4. Blind Review
5. Score Statistics and Outlier Detection
6. Advanced Judge Dashboard

---

# 3. T3.1 Advanced Judge Assignment

Extend the existing `judge_assignments` implementation.

### Features

- Track-aware judge assignment.
- Workload balancing.
- Prevent assignment to the judge's own team.
- Prevent assignment to conflicted projects.
- Prevent duplicate judge-project assignments.
- Batch assignment.
- Organizer reassignment.
- Assignment status tracking.

### Flow

```text
Project -> Track -> Eligible Judges
       -> Remove conflicts
       -> Remove own-team judges
       -> Check workload
       -> Assign
```

### Status

```text
ASSIGNED
IN_PROGRESS
COMPLETED
RECUSED
CANCELLED
```

### Model Extension

Extend the existing assignment model where possible:

```text
id
judge_id
submission_id
assigned_at
status
completed_at
assignment_round
```

### APIs

```http
POST /judge-assignments
POST /judge-assignments/batch
GET /judges/me/assignments
GET /hackathons/{id}/assignments
DELETE /judge-assignments/{id}
```

---

# 4. T3.2 Pairwise Judging

Implement project-vs-project evaluation.

### New Model

`pairwise_evaluations`

```text
id
hackathon_id
judge_id
submission_a_id
submission_b_id
winner_submission_id
reason
status
created_at
completed_at
```

### Rules

- A submission cannot be compared with itself.
- Judges cannot compare their own team's project.
- Judges cannot evaluate conflicted projects.
- The same judge cannot submit the same pair twice.
- Judges can access only their own pairwise evaluations.
- Organizers/admins can access all pairwise evaluations.
- Submitted/locked evaluations cannot be edited.

### Status

```text
ASSIGNED
IN_PROGRESS
SUBMITTED
LOCKED
CANCELLED
```

### APIs

```http
POST /pairwise-evaluations
GET /judges/me/pairwise-evaluations
GET /pairwise-evaluations/{id}
PUT /pairwise-evaluations/{id}
POST /pairwise-evaluations/{id}/submit
POST /pairwise-evaluations/{id}/lock
GET /hackathons/{id}/pairwise-evaluations
GET /hackathons/{id}/pairwise-progress
```

---

# 5. T3.3 Judge Calibration

Create a calibration workflow.

### Models

`calibration_sets`

```text
id
hackathon_id
name
status
created_at
```

`calibration_projects`

```text
id
calibration_set_id
submission_id
expected_score
created_at
```

`calibration_results`

```text
id
calibration_set_id
judge_id
submission_id
score
deviation
completed_at
```

### Flow

```text
Organizer creates calibration set
        ↓
Reference projects selected
        ↓
Judges evaluate reference projects
        ↓
System compares scores
        ↓
Deviation calculated
        ↓
Organizer views calibration statistics
```

### APIs

```http
POST /hackathons/{id}/calibration-sets
GET /hackathons/{id}/calibration-sets
POST /calibration-sets/{id}/projects
POST /calibration-sets/{id}/assign
POST /calibration-results
GET /judges/me/calibration
GET /hackathons/{id}/calibration
```

---

# 6. T3.4 Blind Review

Support hiding sensitive team information from judges.

### Submission Extension

```text
blind_review_enabled
```

### Rule

Blind review must be enforced at the API response layer. The frontend must not merely hide fields.

Example:

```json
{
  "submission_id": "P001",
  "title": "Project Alpha",
  "track": "AI",
  "description": "...",
  "repository_url": "...",
  "team_name": null
}
```

---

# 7. T3.5 Score Statistics and Outlier Detection

Calculate:

### Project

```text
average
median
minimum
maximum
standard_deviation
score_count
```

### Judge

```text
average_score
score_variance
completed_reviews
average_deviation
```

### APIs

```http
GET /hackathons/{id}/score-statistics
GET /hackathons/{id}/score-outliers
GET /judges/{id}/score-statistics
```

Outlier detection is informational and must not silently modify submitted scores.

---

# 8. T3.6 Advanced Judge Dashboard

Extend:

```http
GET /judges/me/dashboard
GET /hackathons/{id}/judging-progress
```

Include:

```text
assigned projects
completed reviews
pending reviews
completion percentage
pairwise pending
calibration status
average score
judge workload
pairwise progress
calibration progress
```

---

# 9. T4 Scope

T4 adds:

1. Conflict of Interest / Recusal
2. Advanced Audit Trail
3. Result Lifecycle
4. Organizer Analytics
5. Integrity Checks
6. Organizer Dashboard
7. Advanced Exports

---

# 10. T4.1 Conflict of Interest / Recusal

### New Model

`judge_conflicts`

```text
id
judge_id
submission_id
reason
status
reported_at
resolved_at
resolved_by
```

### Status

```text
DECLARED
APPROVED
REJECTED
RESOLVED
```

### APIs

```http
POST /judges/me/conflicts
GET /judges/me/conflicts
GET /hackathons/{id}/conflicts
PUT /judge-conflicts/{id}
POST /judge-conflicts/{id}/resolve
POST /judge-conflicts/{id}/reject
```

The assignment service must automatically exclude judges with active conflicts.

---

# 11. T4.2 Advanced Audit Trail

Extend the existing `audit_logs` implementation.

### Actions

```text
LOGIN
LOGOUT
SUBMISSION_CREATED
SUBMISSION_UPDATED
SUBMISSION_LOCKED
JUDGE_ASSIGNED
JUDGE_REASSIGNED
CONFLICT_DECLARED
REVIEW_CREATED
SCORE_CREATED
SCORE_UPDATED
REVIEW_LOCKED
RESULT_CALCULATED
RESULT_PUBLISHED
REGISTRATION_CREATED
PAYMENT_UPDATED
```

### Fields

```text
id
actor_id
action
entity_type
entity_id
old_value
new_value
ip_address
user_agent
created_at
```

### API

```http
GET /hackathons/{id}/audit-logs
```

Support filters:

```text
action
actor_id
entity_type
from
to
```

---

# 12. T4.3 Result Lifecycle

Use:

```text
DRAFT
CALCULATED
UNDER_REVIEW
APPROVED
PUBLISHED
LOCKED
```

### APIs

```http
POST /hackathons/{id}/results/calculate
POST /hackathons/{id}/results/review
POST /hackathons/{id}/results/approve
POST /hackathons/{id}/results/publish
POST /hackathons/{id}/results/lock
```

### Rules

- Only organizer/admin can calculate, approve, and publish.
- Published results are auditable.
- Locked results cannot be modified through normal APIs.
- Every lifecycle transition creates an audit log.

---

# 13. T4.4 Organizer Analytics

### Submission Analytics

```http
GET /hackathons/{id}/analytics/submissions
```

Return:

```text
total submissions
submitted
draft
locked
by track
by technology
```

### Judging Analytics

```http
GET /hackathons/{id}/analytics/judging
```

Return:

```text
total reviews
completed
pending
completion percentage
average score
score distribution
judge workload
```

### Track Analytics

```http
GET /hackathons/{id}/analytics/tracks
```

Return:

```text
track
projects
judges
reviews
average score
completion percentage
```

Analytics must enforce role authorization.

---

# 14. T4.5 Integrity Checks

Create an `IntegrityService`.

### Assignment Checks

```text
Judge assigned to own team
Judge assigned to conflicted project
Duplicate assignment
```

### Review Checks

```text
Missing scores
Incomplete reviews
Duplicate reviews
Locked review modified
```

### Score Checks

```text
Extreme score deviation
Unusually identical scores
Missing criteria
Score outside rubric range
```

### Submission Checks

```text
Duplicate repository
Duplicate submission
Submission after deadline
Invalid track
```

### APIs

```http
GET /hackathons/{id}/integrity/checks
GET /hackathons/{id}/integrity/alerts
POST /hackathons/{id}/integrity/run
```

Integrity alerts must be explainable and auditable.

---

# 15. T4.6 Organizer Dashboard Backend

### API

```http
GET /hackathons/{id}/organizer/dashboard
```

Response:

```json
{
  "registrations": {},
  "teams": {},
  "submissions": {},
  "judging": {},
  "conflicts": {},
  "integrity": {},
  "results": {}
}
```

The frontend must consume this through the API and never access the database directly.

---

# 16. T4.7 Advanced Exports

Organizer-only:

```http
GET /hackathons/{id}/exports/results.csv
GET /hackathons/{id}/exports/judging.csv
GET /hackathons/{id}/exports/judges.csv
GET /hackathons/{id}/exports/audit.csv
GET /hackathons/{id}/exports/integrity.csv
```

---

# 17. Database Changes

Prefer extending existing models.

New models:

```text
pairwise_evaluations
calibration_sets
calibration_projects
calibration_results
judge_conflicts
```

Extend where possible:

```text
judge_assignments
reviews
scores
results
audit_logs
submissions
hackathons
```

Every change requires:

```text
Alembic migration
↓
Migration test
↓
Existing T1/T2 tests
↓
New T3/T4 tests
```

Do not create duplicate models unnecessarily.

---

# 18. Authorization Matrix

| Feature | Participant | Judge | Organizer | Admin |
|---|---:|---:|---:|---:|
| Own submission | Yes | - | Yes | Yes |
| Public gallery | Yes | Yes | Yes | Yes |
| Own assignments | - | Yes | Yes | Yes |
| Own reviews | - | Yes | Yes | Yes |
| Other judge reviews | No | No | Yes | Yes |
| Pairwise evaluation | No | Own only | Yes | Yes |
| Calibration | No | Own | Yes | Yes |
| Declare conflict | No | Yes | Yes | Yes |
| Resolve conflict | No | No | Yes | Yes |
| Analytics | No | Limited | Yes | Yes |
| Audit logs | No | No | Yes | Yes |
| Calculate results | No | No | Yes | Yes |
| Publish results | No | No | Yes | Yes |
| Advanced exports | No | Limited | Yes | Yes |

---

# 19. Implementation Order

```text
T3.1 Advanced Judge Assignment
        ↓
T3.2 Pairwise Judging
        ↓
T3.3 Judge Calibration
        ↓
T3.4 Blind Review
        ↓
T3.5 Score Statistics / Outliers
        ↓
T3.6 Judge Dashboard
        ↓
     RUN TESTS
        ↓
T4.1 Conflict / Recusal
        ↓
T4.2 Advanced Audit
        ↓
T4.3 Result Lifecycle
        ↓
T4.4 Analytics
        ↓
T4.5 Integrity Checks
        ↓
T4.6 Organizer Dashboard
        ↓
T4.7 Advanced Exports
        ↓
     FULL TEST
```

---

# 20. Testing Requirements

### T3

```text
test_advanced_assignment.py
test_pairwise_judging.py
test_calibration.py
test_blind_review.py
test_score_statistics.py
test_judge_dashboard.py
```

### T4

```text
test_conflicts.py
test_audit_trail.py
test_result_lifecycle.py
test_analytics.py
test_integrity.py
test_organizer_dashboard.py
test_advanced_exports.py
```

After every phase:

```bash
pytest
```

Existing T1/T2 tests must continue passing.

---

# 21. Final Checklist

## T3

- [ ] Advanced judge assignment works.
- [ ] Workload balancing works.
- [ ] Conflict checks happen before assignment.
- [ ] Pairwise judging works.
- [ ] Duplicate pairs are rejected.
- [ ] Judges cannot access other judges' pairwise evaluations.
- [ ] Calibration workflow works.
- [ ] Blind review is enforced at API level.
- [ ] Score statistics are calculated.
- [ ] Outliers can be identified.
- [ ] Judge dashboard exposes authorized progress.
- [ ] All T1/T2 tests still pass.

## T4

- [ ] Conflict declaration works.
- [ ] Recusal prevents assignment.
- [ ] Audit trail captures important actions.
- [ ] Result lifecycle is enforced.
- [ ] Published/locked results are protected.
- [ ] Organizer analytics work.
- [ ] Integrity checks work.
- [ ] Organizer dashboard works.
- [ ] Advanced exports work.
- [ ] Authorization is enforced on every endpoint.
- [ ] All T1/T2/T3 tests still pass.

---

# 22. Antigravity Master Instruction

```text
Extend the existing Dogfood FastAPI + PostgreSQL backend with
the T3 and T4 capabilities defined in this document.

DO NOT rewrite the existing T1/T2 implementation.
DO NOT remove or rename existing routes.
DO NOT break existing acceptance tests.
DO NOT replace the current architecture.

Implement one phase at a time.

For every phase:
1. Inspect the existing implementation first.
2. Reuse existing models/services/repositories where possible.
3. Add or modify SQLAlchemy models only when required.
4. Create an Alembic migration.
5. Add Pydantic schemas.
6. Add service-layer business logic.
7. Add repository methods when required.
8. Add FastAPI routes.
9. Add backend authorization.
10. Add automated tests.
11. Run the new tests.
12. Run the complete existing test suite.
13. Fix regressions before moving to the next phase.

Start with T3.1 Advanced Judge Assignment.

Do not implement T3.2 until T3.1 tests pass.
Do not implement T4 until all T3 tests pass.
Do not add infrastructure that is not required by this plan.
```

---

## Scope Note

This document is the T3/T4 backend extension plan for the product architecture. It should not be treated as a claim that every listed feature is an official Dogfood acceptance test unless the organizer's tier specification explicitly defines it as such.
