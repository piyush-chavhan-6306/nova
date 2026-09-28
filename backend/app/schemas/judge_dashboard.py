from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class JudgeDashboardResponse(BaseModel):
    judge_id: str
    assigned_projects: int
    completed_reviews: int
    pending_reviews: int
    completion_percentage: float
    pairwise_pending: int
    calibration_status: str
    average_score: float


class JudgeWorkloadItem(BaseModel):
    judge_id: str
    judge_name: str
    assigned_count: int
    completed_count: int
    completion_percentage: float


class HackathonJudgingProgressResponse(BaseModel):
    hackathon_id: str
    total_submissions: int
    total_assignments: int
    completed_assignments: int
    pending_assignments: int
    completion_percentage: float
    judge_workload: List[JudgeWorkloadItem]
    pairwise_completed_pairs: int
    calibration_completed_count: int
