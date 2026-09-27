from typing import List
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from app.repositories.hackathon_repository import HackathonRepository
from app.schemas.hackathon import HackathonCreate, HackathonUpdate, HackathonResponse, HackathonDetailResponse
from app.schemas.track import TrackCreate, TrackResponse


class EventService:
    def __init__(self, db: Session):
        self.repo = HackathonRepository(db)

    def list_hackathons(self, skip: int = 0, limit: int = 100) -> List[HackathonResponse]:
        hackathons = self.repo.list_hackathons(skip=skip, limit=limit)
        return [HackathonResponse.model_validate(h) for h in hackathons]

    def get_hackathon(self, hackathon_id: str) -> HackathonDetailResponse:
        hackathon = self.repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{hackathon_id}' not found")
        tracks = self.repo.list_tracks_for_hackathon(hackathon_id)
        
        detail = HackathonDetailResponse.model_validate(hackathon)
        detail.tracks = [TrackResponse.model_validate(t) for t in tracks]
        return detail

    def create_hackathon(self, hackathon_in: HackathonCreate) -> HackathonResponse:
        hackathon = self.repo.create(hackathon_in)
        return HackathonResponse.model_validate(hackathon)

    def update_hackathon(self, hackathon_id: str, hackathon_in: HackathonUpdate) -> HackathonResponse:
        hackathon = self.repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{hackathon_id}' not found")
        updated = self.repo.update(hackathon, hackathon_in)
        return HackathonResponse.model_validate(updated)

    def list_tracks(self, hackathon_id: str) -> List[TrackResponse]:
        hackathon = self.repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{hackathon_id}' not found")
        tracks = self.repo.list_tracks_for_hackathon(hackathon_id)
        return [TrackResponse.model_validate(t) for t in tracks]

    def create_track(self, hackathon_id: str, track_in: TrackCreate) -> TrackResponse:
        hackathon = self.repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{hackathon_id}' not found")
        track = self.repo.create_track(hackathon_id, track_in)
        return TrackResponse.model_validate(track)
