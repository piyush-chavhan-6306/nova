# ⚖️ JUDGING.md — Assignment, Scoring, Normalization & Conflict Rules

## 1. Judging System Overview
The **NOVA Hackathon Portal** implements a multi-modal judging architecture supporting standard rubric scoring, pairwise head-to-head comparisons, judge calibration normalization, blind review, outlier detection, and conflict of interest recusal.

---

## 2. Judging Features & Workflows

### 📊 Rubric & Workload Assignments
- **Track Rubrics**: Hackathons define multi-criterion scoring rubrics (e.g., Functionality, Quality, Pitch).
- **Workload Distribution**: Batch assignment algorithm balances project reviews evenly across available judges while respecting track specialties.

### 🔒 Peer Isolation & Privacy
- Judges are strictly isolated: `GET /api/v1/judges/{id}/assignments` enforces backend authorization (`require_judge_peer_isolation`).
- A judge cannot inspect or tamper with peer score submissions (`403 Forbidden`).

### 🙈 Blind Review Mode (T3.4)
- When `hackathon.blind_review_enabled` is set to `true`, submission details served to judges mask author and team metadata (returned as `"Anonymous Team"` and `"ANONYMOUS"`).

### ⚔️ Pairwise Evaluation Engine (T3.2)
- Judges perform head-to-head project comparisons (`submission_a` vs `submission_b`).
- Wins and losses are aggregated to compute relative win rates and rank projects using win-ratio algorithms.

### 🎯 Judge Calibration & Score Normalization (T3.3)
- Benchmark project calibration sets establish baseline judge scoring tendencies.
- Standard deviation and mean shifts are calculated per judge to adjust for harsh or lenient grading styles.

### 📈 Score Statistics & Outliers (T3.5)
- Automated statistical analysis calculates mean, median, and standard deviation per project and per judge.
- Anomaly detection flags scores deviating by more than 2 standard deviations (`> 2 stddev`) for organizer audit.

### ⚠️ Conflict of Interest & Recusal Workflow (T4.1)
- Judges can declare conflicts of interest (`DECLARED`).
- The engine automatically revokes active assignments for conflicting submissions and alerts organizers.

### 🔒 Results Lifecycle State Machine (T4.3)
- States: `DRAFT` ➔ `CALCULATED` ➔ `UNDER_REVIEW` ➔ `APPROVED` ➔ `PUBLISHED` ➔ `LOCKED`.
- Final CSV results export is locked to prevent unauthorized modifications after event closure.
