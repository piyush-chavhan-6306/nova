from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, UserIdentity
from app.schemas.result import LeaderboardResponse
from app.services.scoring_service import ScoringService

router = APIRouter(tags=["Results & Leaderboard"])


@router.post("/hackathons/{hackathon_id}/results/calculate", response_model=LeaderboardResponse)
def calculate_results(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Calculate and publish scores and rankings for a hackathon."""
    service = ScoringService(db)
    return service.calculate_leaderboard(hackathon_id, current_user=current_user)


@router.post("/hackathons/{hackathon_id}/results/review", response_model=LeaderboardResponse)
def mark_results_under_review(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark hackathon results as UNDER_REVIEW."""
    service = ScoringService(db)
    return service.transition_result_status(hackathon_id, "UNDER_REVIEW", current_user)


@router.post("/hackathons/{hackathon_id}/results/approve", response_model=LeaderboardResponse)
def approve_results(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve hackathon results."""
    service = ScoringService(db)
    return service.transition_result_status(hackathon_id, "APPROVED", current_user)


@router.post("/hackathons/{hackathon_id}/results/publish", response_model=LeaderboardResponse)
def publish_results(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Publish hackathon results."""
    service = ScoringService(db)
    return service.transition_result_status(hackathon_id, "PUBLISHED", current_user)


@router.post("/hackathons/{hackathon_id}/results/lock", response_model=LeaderboardResponse)
def lock_results(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lock hackathon results against further modifications."""
    service = ScoringService(db)
    return service.transition_result_status(hackathon_id, "LOCKED", current_user)


@router.get("/hackathons/{hackathon_id}/results", response_model=LeaderboardResponse)
def get_leaderboard(
    hackathon_id: str,
    db: Session = Depends(get_db)
):
    """View the leaderboard and final results for a hackathon."""
    service = ScoringService(db)
    return service.get_leaderboard(hackathon_id)


@router.get("/hackathons/{hackathon_id}/results/export")
def export_results_csv(
    hackathon_id: str,
    db: Session = Depends(get_db)
):
    """Export hackathon leaderboard results as a downloadable CSV file (T2 Requirement)."""
    service = ScoringService(db)
    csv_content = service.export_csv(hackathon_id)
    
    filename = f"hackathon_{hackathon_id}_results.csv"
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }
    return Response(content=csv_content, media_type="text/csv", headers=headers)
