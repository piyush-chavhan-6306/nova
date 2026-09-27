from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict, Field
from app.utils.enums import ReviewStatus


class JudgeAssignmentCreate(BaseModel):
    submission_id: str
    judge_id: str


class JudgeAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    judge_id: str
    submission_id: str
    assigned_at: datetime


class ScoreItem(BaseModel):
    criterion_id: str
    score: float = Field(..., ge=0, le=100)
    comment: Optional[str] = None


class ReviewCreate(BaseModel):
    assignment_id: Optional[str] = None
    submission_id: str
    comment: Optional[str] = None
    scores: List[ScoreItem] = []


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    assignment_id: Optional[str] = None
    judge_id: str
    submission_id: str
    status: ReviewStatus
    comment: Optional[str] = None
    submitted_at: Optional[datetime] = None
    created_at: datetime
