from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class SubmissionAnalyticsResponse(BaseModel):
    hackathon_id: str
    total_submissions: int
    submitted: int
    draft: int
    locked: int
    by_track: Dict[str, int]
    by_technology: Dict[str, int]


class JudgingAnalyticsResponse(BaseModel):
    hackathon_id: str
    total_reviews: int
    completed: int
    pending: int
    completion_percentage: float
    average_score: float
    score_distribution: Dict[str, int]
    judge_workload: List[Dict[str, Any]]


class TrackAnalyticsItem(BaseModel):
    track_id: str
    track_name: str
    projects_count: int
    judges_count: int
    reviews_count: int
    average_score: float
    completion_percentage: float


class IntegrityAlertItem(BaseModel):
    alert_type: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    message: str
    entity_id: Optional[str] = None


class IntegrityCheckResponse(BaseModel):
    hackathon_id: str
    total_checks: int
    alerts_count: int
    alerts: List[IntegrityAlertItem]


class OrganizerDashboardResponse(BaseModel):
    hackathon_id: str
    registrations: Dict[str, Any]
    teams: Dict[str, Any]
    submissions: Dict[str, Any]
    judging: Dict[str, Any]
    conflicts: Dict[str, Any]
    integrity: Dict[str, Any]
    results: Dict[str, Any]
