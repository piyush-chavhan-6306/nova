from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_organizer, verify_hackathon_owner, UserIdentity
from app.schemas.hackathon import HackathonCreate, HackathonUpdate, HackathonResponse, HackathonDetailResponse
from app.schemas.track import TrackCreate, TrackResponse, TrackUpdate
from app.schemas.prize import PrizeCreate, PrizeResponse, PrizeUpdate
from app.services.event_service import EventService

router = APIRouter(prefix="/hackathons", tags=["Hackathons"])


@router.get("", response_model=List[HackathonResponse])
def list_hackathons(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search keyword in title or description"),
    status: Optional[str] = Query(None, description="Filter by hackathon status"),
    db: Session = Depends(get_db)
):
    """List active and past hackathons with optional search and status filters (Discovery API)."""
    service = EventService(db)
    return service.list_hackathons(skip=skip, limit=limit, search=search, status=status)


@router.post("", response_model=HackathonResponse, status_code=status.HTTP_201_CREATED)
def create_hackathon(
    hackathon_in: HackathonCreate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Create a new hackathon event (Organizer/Admin only)."""
    service = EventService(db)
    return service.create_hackathon(hackathon_in, creator_id=current_user.id)


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
    """Update existing hackathon metadata (Organizer/Admin only, ownership enforced)."""
    verify_hackathon_owner(hackathon_id, current_user, db)
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
    """Create a new track for a hackathon (Organizer/Admin only, ownership enforced)."""
    verify_hackathon_owner(hackathon_id, current_user, db)
    service = EventService(db)
    return service.create_track(hackathon_id, track_in)

@router.put("/{hackathon_id}/tracks/{track_id}", response_model=TrackResponse)
def update_track(
    hackathon_id: str,
    track_id: str,
    track_in: TrackUpdate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Update a track (Organizer/Admin only, ownership enforced)."""
    verify_hackathon_owner(hackathon_id, current_user, db)
    service = EventService(db)
    return service.update_track(hackathon_id, track_id, track_in)

@router.get("/{hackathon_id}/prizes", response_model=List[PrizeResponse])
def list_prizes(hackathon_id: str, db: Session = Depends(get_db)):
    """List all prizes for a specific hackathon."""
    service = EventService(db)
    return service.list_prizes(hackathon_id)

@router.post("/{hackathon_id}/prizes", response_model=PrizeResponse, status_code=status.HTTP_201_CREATED)
def create_prize(
    hackathon_id: str,
    prize_in: PrizeCreate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Create a new prize (Organizer/Admin only, ownership enforced)."""
    verify_hackathon_owner(hackathon_id, current_user, db)
    service = EventService(db)
    return service.create_prize(hackathon_id, prize_in)

@router.put("/{hackathon_id}/prizes/{prize_id}", response_model=PrizeResponse)
def update_prize(
    hackathon_id: str,
    prize_id: str,
    prize_in: PrizeUpdate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Update a prize (Organizer/Admin only, ownership enforced)."""
    verify_hackathon_owner(hackathon_id, current_user, db)
    service = EventService(db)
    return service.update_prize(hackathon_id, prize_id, prize_in)

@router.delete("/{hackathon_id}/prizes/{prize_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prize(
    hackathon_id: str,
    prize_id: str,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Delete a prize (Organizer/Admin only, ownership enforced)."""
    verify_hackathon_owner(hackathon_id, current_user, db)
    service = EventService(db)
    service.delete_prize(hackathon_id, prize_id)
