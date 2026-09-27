from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_organizer, UserIdentity
from app.schemas.hackathon import HackathonCreate, HackathonUpdate, HackathonResponse, HackathonDetailResponse
from app.schemas.track import TrackCreate, TrackResponse
from app.services.event_service import EventService

router = APIRouter(prefix="/hackathons", tags=["Hackathons"])


@router.get("", response_model=List[HackathonResponse])
def list_hackathons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all active and past hackathons."""
    service = EventService(db)
    return service.list_hackathons(skip=skip, limit=limit)


@router.post("", response_model=HackathonResponse, status_code=status.HTTP_201_CREATED)
def create_hackathon(
    hackathon_in: HackathonCreate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Create a new hackathon event (Organizer/Admin only)."""
    service = EventService(db)
    return service.create_hackathon(hackathon_in)


@router.get("/{hackathon_id}", response_model=HackathonDetailResponse)
def get_hackathon(hackathon_id: str, db: Session = Depends(get_db)):
    """Retrieve detailed hackathon information including tracks."""
    service = EventService(db)
    return service.get_hackathon(hackathon_id)


@router.put("/{hackathon_id}", response_model=HackathonResponse)
def update_hackathon(
    hackathon_id: str,
    hackathon_in: HackathonUpdate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Update existing hackathon metadata (Organizer/Admin only)."""
    service = EventService(db)
    return service.update_hackathon(hackathon_id, hackathon_in)


@router.get("/{hackathon_id}/tracks", response_model=List[TrackResponse])
def list_tracks(hackathon_id: str, db: Session = Depends(get_db)):
    """List all tracks for a specific hackathon."""
    service = EventService(db)
    return service.list_tracks(hackathon_id)


@router.post("/{hackathon_id}/tracks", response_model=TrackResponse, status_code=status.HTTP_201_CREATED)
def create_track(
    hackathon_id: str,
    track_in: TrackCreate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Create a new track for a hackathon (Organizer/Admin only)."""
    service = EventService(db)
    return service.create_track(hackathon_id, track_in)
