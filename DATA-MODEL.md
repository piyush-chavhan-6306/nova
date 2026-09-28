# 🗄️ DATA-MODEL.md — Data Model & Schema Specification

## 1. Schema Overview
The database schema for NOVA is structured around standard relational entities using PostgreSQL and SQLAlchemy ORM.

---

## 2. Core Entities & Relationships

### `users`
- `id` (PK, String): Unique user ID (e.g., `usr_01`, `jdg_01`)
- `email` (String, Unique, Index): Email address
- `name` (String): Full name
- `role` (Enum): `ADMIN`, `ORGANIZER`, `JUDGE`, `PARTICIPANT`

### `hackathons`
- `id` (PK, String): Hackathon ID (e.g., `evt_01`)
- `name` (String): Event title
- `status` (Enum): `DRAFT`, `UPCOMING`, `ACTIVE`, `SUBMISSIONS_CLOSED`, `CLOSED`, `ARCHIVED`
- `submissions_close` (DateTime): ISO 8601 deadline timestamp
- `blind_review_enabled` (Boolean): Anonymization flag
- `results_status` (String): `DRAFT`, `CALCULATED`, `UNDER_REVIEW`, `APPROVED`, `PUBLISHED`, `LOCKED`

### `tracks`
- `id` (PK, String): Track ID
- `hackathon_id` (FK): Parent hackathon
- `name` (String): Track name (e.g., Developer Tools)

### `teams` & `team_members`
- `teams`: `id`, `hackathon_id`, `name`, `created_at`
- `team_members`: `id`, `team_id` (FK), `user_id` (FK), `role` (`CAPTAIN`, `MEMBER`)

### `submissions`
- `id` (PK, String): Submission ID (e.g., `prj_01`)
- `hackathon_id` (FK), `team_id` (FK), `track_id` (FK)
- `title` (String), `summary` (Text), `repo_url` (String), `demo_url` (String)
- `status` (Enum): `DRAFT`, `SUBMITTED`, `LOCKED`
- `submitted_at` (DateTime)

### `judges` & `judge_assignments`
- `judges`: `id` (PK), `user_id` (FK), `hackathon_id` (FK)
- `judge_assignments`: `id` (PK), `judge_id` (FK), `submission_id` (FK), `status` (`PENDING`, `COMPLETED`)

### `reviews` & `scores`
- `reviews`: `id` (PK), `submission_id` (FK), `judge_id` (FK), `status` (`DRAFT`, `SUBMITTED`), `comment` (Text)
- `scores`: `id` (PK), `review_id` (FK), `criterion_name` (String), `score` (Float)

### `judge_conflicts`
- `id` (PK), `judge_id` (FK), `submission_id` (FK), `reason` (Text), `status` (`DECLARED`, `APPROVED`, `REJECTED`, `RESOLVED`)

### `audit_logs`
- `id` (PK), `hackathon_id`, `user_id`, `action`, `target_type`, `target_id`, `details`, `timestamp`

### `results`
- `id` (PK), `hackathon_id`, `submission_id`, `raw_score`, `final_score`, `rank`, `is_published`
