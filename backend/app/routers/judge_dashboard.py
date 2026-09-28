from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, UserIdentity
from app.schemas.judge_dashboard import JudgeDashboardResponse, HackathonJudgingProgressResponse
from app.services.judge_dashboard_service import JudgeDashboardService

router = APIRouter(tags=["Advanced Judge Dashboard"])


@router.get("/judges/me/dashboard", response_model=JudgeDashboardResponse)
def get_my_judge_dashboard(
    hackathon_id: str = Query(...),
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve personal judging metrics, workloads, pairwise status, and calibration progress for logged-in judge."""
    service = JudgeDashboardService(db)
    return service.get_judge_dashboard(current_user, hackathon_id)


@router.get("/hackathons/{hackathon_id}/judging-progress", response_model=HackathonJudgingProgressResponse)
def get_hackathon_judging_progress(
    hackathon_id: str,
    db: Session = Depends(get_db)
):
    """Retrieve aggregate judging completion progress and judge workload matrix for an event."""
    service = JudgeDashboardService(db)
    return service.get_hackathon_judging_progress(hackathon_id)
