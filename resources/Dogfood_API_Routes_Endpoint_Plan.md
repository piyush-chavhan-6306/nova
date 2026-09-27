# Dogfood Hackathon Portal — Complete API Routes / Endpoint Plan

This is the complete API blueprint for the backend.

The routes are designed from:

- Dogfood requirements/specification
- `fixtures.json`
- finalized database schema
- actual product workflow
- T1 + T2 backend scope
- optional organizer-controlled registration/payment
- future T3/T4 extensibility

The frontend will consume these APIs. The frontend is not the source of truth.

---

# 1. Users / Profile

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `GET` | `/users/me` | All | Return the current user's profile and role |
| `GET` | `/users/{user_id}` | Organizer/Admin | Get a user's basic details |
| `PUT` | `/users/me` | All | Update name/profile information |

**Tables:** `users`

> We don't need a login endpoint as a core requirement right now. The backend still needs to identify the caller somehow so authorization can work.

---

# 2. Hackathons / Events

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/hackathons` | Organizer | Create a new hackathon |
| `GET` | `/hackathons` | Public | List available hackathons |
| `GET` | `/hackathons/{id}` | Public | Get event details |
| `PUT` | `/hackathons/{id}` | Organizer | Update event configuration |
| `DELETE` | `/hackathons/{id}` | Organizer | Remove/archive an event |
| `GET` | `/hackathons/{id}/status` | All | Return current event state |

### Important logic

`POST /hackathons` should support things like:

```text
name
description
registration dates
submission dates
team size
tracks
payment_required
registration_fee
currency
```

The status endpoint should determine whether the event is:

```text
DRAFT
UPCOMING
REGISTRATION_OPEN
ACTIVE
SUBMISSIONS_CLOSED
CLOSED
ARCHIVED
```

**Tables:** `hackathons`

---

# 3. Tracks

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/hackathons/{id}/tracks` | Organizer | Create a track |
| `GET` | `/hackathons/{id}/tracks` | Public | List tracks |
| `GET` | `/tracks/{track_id}` | Public | Get track details |
| `PUT` | `/tracks/{track_id}` | Organizer | Update track |
| `DELETE` | `/tracks/{track_id}` | Organizer | Remove/archive track |

**Tables:** `tracks`

---

# 4. Teams

This is an important T1 module.

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/teams` | Participant | Create a team |
| `GET` | `/teams/{team_id}` | Team members | Get team details |
| `PUT` | `/teams/{team_id}` | Team lead | Update team |
| `DELETE` | `/teams/{team_id}` | Team lead | Delete team if allowed |
| `POST` | `/teams/{team_id}/invite` | Team lead | Create/send invitation |
| `GET` | `/team-invitations/{token}` | Participant | View invitation |
| `POST` | `/team-invitations/{token}/accept` | Participant | Join the team |
| `DELETE` | `/teams/{team_id}/members/{user_id}` | Team lead | Remove member |
| `GET` | `/users/me/team` | Participant | Get current user's team |

### Backend must enforce

```text
team size >= minimum
team size <= maximum
same user cannot belong to multiple teams
only team lead can invite/remove
invitation must be valid
event must allow team formation
```

**Tables:**

```text
teams
team_members
team_invitations
users
hackathons
```

---

# 5. Registration — Optional Payment

Since we decided payment should be **organizer-controlled**, registration needs to support both cases.

## Registration

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/hackathons/{id}/registrations` | Participant | Register for an event |
| `GET` | `/hackathons/{id}/registrations/me` | Participant | Get own registration |
| `GET` | `/hackathons/{id}/registrations` | Organizer | View registrations |
| `PUT` | `/registrations/{id}` | Organizer | Update registration status |

## Payment

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/registrations/{id}/payment` | Participant | Create payment order |
| `GET` | `/payments/{id}` | Participant/Organizer | Get payment status |
| `POST` | `/payments/webhook` | Payment provider | Receive payment status |
| `POST` | `/payments/{id}/verify` | Backend | Verify transaction |

### Important flow

For a free event:

```text
Register
   ↓
Confirmed
```

For a paid event:

```text
Register
   ↓
Create payment order
   ↓
Payment Gateway
   ↓
Webhook / verification
   ↓
SUCCESS
   ↓
Registration confirmed
```

**Tables:**

```text
registrations
payments
hackathons
users
```

---

# 6. Submissions

This is one of the biggest modules.

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/submissions` | Team lead | Create project draft |
| `GET` | `/submissions/{id}` | Team members/Judge/Organizer | View submission |
| `PUT` | `/submissions/{id}` | Team lead | Edit draft |
| `DELETE` | `/submissions/{id}` | Team lead | Delete draft |
| `POST` | `/submissions/{id}/submit` | Team lead | Finalize submission |
| `POST` | `/submissions/{id}/lock` | System/Organizer | Lock submission |
| `GET` | `/teams/{team_id}/submission` | Team | Get team's submission |
| `GET` | `/hackathons/{id}/submissions` | Organizer | List all submissions |

### `POST /submissions/{id}/submit` must check:

```text
✓ event is accepting submissions
✓ team is valid
✓ team size is valid
✓ required fields are present
✓ selected track exists
✓ repository URL is valid
✓ submission hasn't already been finalized
✓ deadline hasn't passed
```

Then:

```text
DRAFT
  ↓
SUBMITTED
  ↓
LOCKED
```

**Tables:**

```text
submissions
teams
team_members
tracks
hackathons
```

---

# 7. Submission Checks

This is where our Stitch **pre-flight** UI can connect to the backend without us blindly implementing every fancy check.

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/submissions/{id}/validate` | Team | Run submission validation |
| `GET` | `/submissions/{id}/checks` | Team/Judge/Organizer | Return validation results |

Checks can initially include:

```text
Team eligibility
Required fields
Repository URL
Track
Deadline
Submission status
```

Later we can add GitHub/license/deployment checks if we decide they're useful.

**Tables:** `submission_checks`, `submissions`

---

# 8. Public Gallery

This is separate from private submissions.

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `GET` | `/gallery` | Public | List public projects |
| `GET` | `/gallery/{submission_id}` | Public | Show project details |

Optional filters:

```text
/gallery?track=AI
/gallery?search=health
/gallery?technology=Python
```

Backend should only expose projects that are actually allowed to be public.

**Tables:**

```text
submissions
teams
tracks
```

---

# 9. Judges

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/hackathons/{id}/judges` | Organizer | Add/invite judge |
| `GET` | `/hackathons/{id}/judges` | Organizer | List judges |
| `GET` | `/judges/me` | Judge | Get own judge profile |
| `PUT` | `/judges/{id}` | Organizer | Update judge |
| `DELETE` | `/judges/{id}` | Organizer | Remove/deactivate judge |

**Tables:**

```text
users
judges
hackathons
```

---

# 10. Judge ↔ Track

Because the fixture has judges associated with tracks, we need this.

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/judges/{judge_id}/tracks` | Organizer | Assign judge to track |
| `GET` | `/judges/{judge_id}/tracks` | Organizer/Judge | View assigned tracks |
| `DELETE` | `/judges/{judge_id}/tracks/{track_id}` | Organizer | Remove track assignment |

**Table:** `judge_tracks`

---

# 11. Judge Assignments

This is where projects get assigned to judges.

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/judge-assignments` | Organizer | Assign judge to submission |
| `POST` | `/judge-assignments/batch` | Organizer | Assign multiple projects |
| `GET` | `/judges/me/assignments` | Judge | Show my assigned projects |
| `GET` | `/hackathons/{id}/assignments` | Organizer | View all assignments |
| `DELETE` | `/judge-assignments/{id}` | Organizer | Remove assignment |

### Assignment logic

The service should check:

```text
Judge exists
      ↓
Judge belongs to appropriate track
      ↓
Submission belongs to same event
      ↓
Judge isn't assigned twice
      ↓
Conflict rules (if implemented)
      ↓
Create assignment
```

**Table:** `judge_assignments`

---

# 12. Rubrics

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/hackathons/{id}/rubrics` | Organizer | Create rubric |
| `GET` | `/hackathons/{id}/rubrics` | Organizer/Judge | Get rubric |
| `PUT` | `/rubrics/{id}` | Organizer | Update rubric |
| `POST` | `/rubrics/{id}/criteria` | Organizer | Add criterion |
| `PUT` | `/rubric-criteria/{id}` | Organizer | Update criterion |
| `DELETE` | `/rubric-criteria/{id}` | Organizer | Remove criterion |

Example:

```text
Functionality      40%
Technical Quality  30%
Innovation         30%
```

**Tables:**

```text
rubrics
rubric_criteria
```

---

# 13. Reviews

This is where the judge actually evaluates a project.

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/reviews` | Judge | Start/create review |
| `GET` | `/reviews/{id}` | Assigned judge | Get own review |
| `PUT` | `/reviews/{id}` | Assigned judge | Save draft review |
| `POST` | `/reviews/{id}/submit` | Assigned judge | Submit final review |
| `POST` | `/reviews/{id}/lock` | System/Organizer | Lock review |
| `GET` | `/judges/me/reviews` | Judge | List own reviews |

### Critical authorization

If:

```text
Judge A → Review A
Judge B → Review B
```

then:

```text
Judge A → Review A ✅
Judge A → Review B ❌
Participant → Review A ❌
```

This must be enforced in the **backend**, not merely hidden in the UI.

**Tables:**

```text
reviews
judge_assignments
submissions
users
```

---

# 14. Scores

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `POST` | `/reviews/{id}/scores` | Assigned judge | Add criterion score |
| `PUT` | `/scores/{id}` | Assigned judge | Update score |
| `GET` | `/reviews/{id}/scores` | Assigned judge/Organizer | Get permitted scores |

Example:

```text
Functionality = 4.5
Quality       = 4
Innovation    = 5
```

The backend calculates the weighted review score.

**Tables:**

```text
scores
reviews
rubric_criteria
```

---

# 15. Judge Dashboard / Progress

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `GET` | `/judges/me/dashboard` | Judge | Show assignments, completed/pending |
| `GET` | `/hackathons/{id}/judging-progress` | Organizer | Show overall judging progress |

Example response concept:

```text
Assigned: 10
Completed: 6
Pending: 4
```

**Tables:**

```text
judge_assignments
reviews
scores
```

---

# 16. Results

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `GET` | `/hackathons/{id}/results` | Organizer | Get calculated results |
| `GET` | `/submissions/{id}/result` | Organizer | Get project result |
| `POST` | `/hackathons/{id}/results/calculate` | Organizer | Calculate results |
| `POST` | `/hackathons/{id}/results/publish` | Organizer | Publish results |

This is where later we can plug in:

```text
raw score
     ↓
normalization
     ↓
weighted score
     ↓
ranking
```

So T3/T4 can extend this without changing our basic judging structure.

---

# 17. CSV Export

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `GET` | `/hackathons/{id}/results/export` | Organizer | Export judging results as CSV |
| `GET` | `/hackathons/{id}/submissions/export` | Organizer | Export submission data |
| `GET` | `/hackathons/{id}/judges/export` | Organizer | Export judge data |

This is particularly important because organizer CSV export is part of the official acceptance behavior.

---

# 18. Audit Logs

| Method | Endpoint | Role | What it must do |
|---|---|---|---|
| `GET` | `/hackathons/{id}/audit-logs` | Organizer/Admin | View important system actions |

We should also **automatically create audit logs from services**, rather than relying on someone manually calling the endpoint.

For example:

```text
Judge assigned
Submission locked
Score submitted
Result published
Payment completed
```

**Table:** `audit_logs`

---

# 19. Optional Payment Module

These are already accounted for in our schema.

```text
POST /registrations/{id}/payment
GET  /payments/{id}
POST /payments/webhook
POST /payments/{id}/verify
```

This module can remain disabled when:

```text
hackathons.payment_required = false
```

---

# 20. Complete Backend Route Picture

```text
                         FASTAPI
                            │
 ┌──────────────────────────┼──────────────────────────┐
 │                          │                          │
 ↓                          ↓                          ↓
EVENT / T1               PARTICIPATION              JUDGING / T2
 │                          │                          │
 ├─ Hackathons              ├─ Teams                  ├─ Judges
 ├─ Tracks                  ├─ Members                ├─ Judge Tracks
 └─ Gallery                 ├─ Registration            ├─ Assignments
                            └─ Submissions             ├─ Rubrics
                                                       ├─ Reviews
                                                       ├─ Scores
                                                       └─ Results
 │                          │                          │
 └──────────────────────────┼──────────────────────────┘
                            ↓
                       PostgreSQL
                            │
              ┌─────────────┴─────────────┐
              ↓                           ↓
         Audit Logs                 Optional Payments
```

---

# 21. Implementation Order

**Don't build these all at once.**

```text
PHASE 1
Hackathons + Tracks
       ↓
PHASE 2
Teams + Members
       ↓
PHASE 3
Submissions + Gallery
       ↓
PHASE 4
Judges + Assignments
       ↓
PHASE 5
Rubrics + Reviews + Scores
       ↓
PHASE 6
Results + CSV
       ↓
PHASE 7
Registration + Optional Payment
       ↓
PHASE 8
Audit + advanced features
```

This gives us a **complete route map now**, while keeping the actual coding manageable. And when we eventually move to T3/T4, we can add new routes around the existing `services → repositories → database` architecture rather than rewriting these endpoints.
