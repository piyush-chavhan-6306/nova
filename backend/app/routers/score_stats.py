from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.score_stats import (
    ScoreStatisticsResponse, JudgeScoreStatisticsResponse, OutlierDetectionResponse
)
from app.services.score_stats_service import ScoreStatsService

router = APIRouter(tags=["Score Statistics"])


@router.get("/hackathons/{hackathon_id}/score-statistics", response_model=ScoreStatisticsResponse)
def get_hackathon_score_statistics(
    hackathon_id: str,
    db: Session = Depends(get_db)
):
    """Calculate statistical distribution (mean, median, stddev, min, max) of scores for a hackathon."""
    service = ScoreStatsService(db)
    return service.get_hackathon_statistics(hackathon_id)


@router.get("/hackathons/{hackathon_id}/score-outliers", response_model=OutlierDetectionResponse)
def get_hackathon_score_outliers(
    hackathon_id: str,
    db: Session = Depends(get_db)
):
    """Detect statistical outliers in project review scores (>2 stddev from mean)."""
    service = ScoreStatsService(db)
    return service.get_score_outliers(hackathon_id)


@router.get("/judges/{judge_id}/score-statistics", response_model=JudgeScoreStatisticsResponse)
def get_judge_score_statistics(
    judge_id: str,
    db: Session = Depends(get_db)
):
    """Retrieve scoring stats, variance, and deviation for a specific judge."""
    service = ScoreStatsService(db)
    return service.get_judge_statistics(judge_id)
