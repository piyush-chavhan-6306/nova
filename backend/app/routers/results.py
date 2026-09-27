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
    return service.calculate_leaderboard(hackathon_id)


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
