from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, UserIdentity
from app.schemas.calibration import (
    CalibrationSetCreate, CalibrationProjectCreate, CalibrationResultCreate,
    CalibrationSetResponse, CalibrationProjectResponse, CalibrationResultResponse, CalibrationSummaryResponse
)
from app.services.calibration_service import CalibrationService

router = APIRouter(tags=["Judge Calibration"])


@router.post("/hackathons/{hackathon_id}/calibration-sets", response_model=CalibrationSetResponse, status_code=status.HTTP_201_CREATED)
def create_calibration_set(
    hackathon_id: str,
    set_in: CalibrationSetCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new calibration benchmark set for a hackathon."""
    service = CalibrationService(db)
    return service.create_set(hackathon_id, set_in, current_user)


@router.get("/hackathons/{hackathon_id}/calibration-sets", response_model=List[CalibrationSetResponse])
def get_calibration_sets(
    hackathon_id: str,
    db: Session = Depends(get_db)
):
    """List all calibration sets configured for a hackathon."""
    service = CalibrationService(db)
    return service.list_sets(hackathon_id)


@router.post("/calibration-sets/{set_id}/projects", response_model=CalibrationProjectResponse, status_code=status.HTTP_201_CREATED)
def add_calibration_project(
    set_id: str,
    proj_in: CalibrationProjectCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a reference project with expected score to a calibration set."""
    service = CalibrationService(db)
    return service.add_project(set_id, proj_in, current_user)


@router.post("/calibration-results", response_model=CalibrationResultResponse, status_code=status.HTTP_201_CREATED)
def record_calibration_result(
    res_in: CalibrationResultCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit evaluation for a calibration reference project."""
    service = CalibrationService(db)
    return service.record_result(res_in, current_user)


@router.get("/judges/me/calibration", response_model=CalibrationSummaryResponse)
def get_my_calibration(
    hackathon_id: str = Query(...),
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve calibration status and average deviation for current judge."""
    service = CalibrationService(db)
    return service.get_judge_calibration(current_user, hackathon_id)


@router.get("/hackathons/{hackathon_id}/calibration", response_model=List[CalibrationResultResponse])
def get_hackathon_calibration(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """View overall judge calibration statistics for a hackathon."""
    service = CalibrationService(db)
    return service.get_hackathon_calibration(hackathon_id, current_user)
