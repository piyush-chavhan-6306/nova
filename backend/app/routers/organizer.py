from typing import List, Optional
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_user_optional, verify_hackathon_owner, UserIdentity
from app.utils.enums import UserRole
from app.schemas.organizer_analytics import (
    SubmissionAnalyticsResponse, JudgingAnalyticsResponse,
    TrackAnalyticsItem, IntegrityCheckResponse, OrganizerDashboardResponse
)
from app.services.organizer_service import OrganizerService
from app.services.scoring_service import ScoringService

router = APIRouter(tags=["Organizer Dashboard, Analytics & Exports"])


# --- T4.4 Analytics ---
@router.get("/hackathons/{hackathon_id}/analytics/submissions", response_model=SubmissionAnalyticsResponse)
def get_submission_analytics(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve submission analytics breakdown by status, track, and tech stack."""
    service = OrganizerService(db)
    return service.get_submission_analytics(hackathon_id, current_user)


@router.get("/hackathons/{hackathon_id}/analytics/judging", response_model=JudgingAnalyticsResponse)
def get_judging_analytics(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve judging analytics, score distribution, and workload matrices."""
    service = OrganizerService(db)
    return service.get_judging_analytics(hackathon_id, current_user)


@router.get("/hackathons/{hackathon_id}/analytics/tracks", response_model=List[TrackAnalyticsItem])
def get_track_analytics(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve track-level analytics and project/judge performance metrics."""
    service = OrganizerService(db)
    return service.get_track_analytics(hackathon_id, current_user)


# --- T4.5 Integrity Checks ---
@router.get("/hackathons/{hackathon_id}/integrity/checks", response_model=IntegrityCheckResponse)
@router.get("/hackathons/{hackathon_id}/integrity/alerts", response_model=IntegrityCheckResponse)
@router.post("/hackathons/{hackathon_id}/integrity/run", response_model=IntegrityCheckResponse)
def get_integrity_checks(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Run automated integrity checks and retrieve audit alerts."""
    service = OrganizerService(db)
    return service.run_integrity_checks(hackathon_id, current_user)


# --- T4.6 Organizer Dashboard ---
@router.get("/hackathons/{hackathon_id}/organizer/dashboard", response_model=OrganizerDashboardResponse)
def get_organizer_dashboard(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve top-level organizer executive summary dashboard metrics."""
    service = OrganizerService(db)
    return service.get_organizer_dashboard(hackathon_id, current_user)


# --- T4.7 Advanced Exports ---
@router.get("/hackathons/{hackathon_id}/exports/results.csv")
def export_results_csv(
    hackathon_id: str,
    current_user: Optional[UserIdentity] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Export final leaderboard results as a downloadable CSV."""
    if current_user and current_user.role == UserRole.ORGANIZER:
        verify_hackathon_owner(hackathon_id, current_user, db)
    scoring_service = ScoringService(db)
    csv_content = scoring_service.export_csv(hackathon_id)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="results_{hackathon_id}.csv"'}
    )


@router.get("/hackathons/{hackathon_id}/exports/judging.csv")
def export_judging_csv(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export full judging review details as a downloadable CSV."""
    service = OrganizerService(db)
    csv_content = service.export_judging_csv(hackathon_id, current_user)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="judging_{hackathon_id}.csv"'}
    )


@router.get("/hackathons/{hackathon_id}/exports/judges.csv")
def export_judges_csv(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export judge roster and assignment counts as CSV."""
    service = OrganizerService(db)
    csv_content = service.export_judges_csv(hackathon_id, current_user)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="judges_{hackathon_id}.csv"'}
    )


@router.get("/hackathons/{hackathon_id}/exports/audit.csv")
def export_audit_csv(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export system audit trail for event as CSV."""
    service = OrganizerService(db)
    csv_content = service.export_audit_csv(hackathon_id, current_user)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="audit_{hackathon_id}.csv"'}
    )


@router.get("/hackathons/{hackathon_id}/exports/integrity.csv")
def export_integrity_csv(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export integrity checks and alerts log as CSV."""
    service = OrganizerService(db)
    csv_content = service.export_integrity_csv(hackathon_id, current_user)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="integrity_{hackathon_id}.csv"'}
    )
