from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.utils.enums import PairwiseStatus


class PairwiseEvaluationCreate(BaseModel):
    hackathon_id: str
    submission_a_id: str
    submission_b_id: str
    judge_id: Optional[str] = None


class PairwiseEvaluationUpdate(BaseModel):
    winner_submission_id: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[PairwiseStatus] = None


class PairwiseEvaluationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    hackathon_id: str
    judge_id: str
    submission_a_id: str
    submission_b_id: str
    winner_submission_id: Optional[str] = None
    reason: Optional[str] = None
    status: PairwiseStatus
    created_at: datetime
    completed_at: Optional[datetime] = None


class PairwiseProgressResponse(BaseModel):
    total_pairs: int
    completed_pairs: int
    completion_percentage: float
