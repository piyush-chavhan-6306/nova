from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ScoreStatisticsResponse(BaseModel):
    hackathon_id: str
    average: float
    median: float
    minimum: float
    maximum: float
    standard_deviation: float
    score_count: int


class JudgeScoreStatisticsResponse(BaseModel):
    judge_id: str
    average_score: float
    score_variance: float
    completed_reviews: int
    average_deviation: float


class OutlierScoreItem(BaseModel):
    review_id: str
    submission_id: str
    judge_id: str
    total_score: float
    mean_score: float
    deviation: float
    is_outlier: bool


class OutlierDetectionResponse(BaseModel):
    hackathon_id: str
    outliers_count: int
    outliers: List[OutlierScoreItem]
