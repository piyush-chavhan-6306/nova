from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from app.repositories.hackathon_repository import HackathonRepository
from app.schemas.hackathon import HackathonCreate, HackathonUpdate, HackathonResponse, HackathonDetailResponse
from app.schemas.track import TrackCreate, TrackResponse, TrackUpdate
from app.schemas.prize import PrizeCreate, PrizeResponse, PrizeUpdate


class EventService:
    def __init__(self, db: Session):
        self.repo = HackathonRepository(db)

    def list_hackathons(self, skip: int = 0, limit: int = 100, search: Optional[str] = None, status: Optional[str] = None) -> List[HackathonResponse]:
        hackathons = self.repo.list_hackathons(skip=skip, limit=limit, search=search, status=status)
        return [HackathonResponse.model_validate(h) for h in hackathons]

    def get_hackathon(self, hackathon_id: str) -> HackathonDetailResponse:
        hackathon = self.repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{hackathon_id}' not found")
        tracks = self.repo.list_tracks_for_hackathon(hackathon_id)
        prizes = self.repo.list_prizes_for_hackathon(hackathon_id)
        
        detail = HackathonDetailResponse.model_validate(hackathon)
        detail.tracks = [TrackResponse.model_validate(t) for t in tracks]
        detail.prizes = [PrizeResponse.model_validate(p) for p in prizes]
        return detail

    def create_hackathon(self, hackathon_in: HackathonCreate, creator_id: Optional[str] = None) -> HackathonResponse:
        hackathon = self.repo.create(hackathon_in, creator_id=creator_id)
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

    def update_track(self, hackathon_id: str, track_id: str, track_in: TrackUpdate) -> TrackResponse:
        hackathon = self.repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{hackathon_id}' not found")
        track = self.repo.get_track_by_id(track_id)
        if not track or track.hackathon_id != hackathon_id:
            raise NotFoundException(f"Track '{track_id}' not found")
        updated = self.repo.update_track(track, track_in)
        return TrackResponse.model_validate(updated)

    def list_prizes(self, hackathon_id: str) -> List[PrizeResponse]:
        hackathon = self.repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{hackathon_id}' not found")
        prizes = self.repo.list_prizes_for_hackathon(hackathon_id)
        return [PrizeResponse.model_validate(p) for p in prizes]

    def create_prize(self, hackathon_id: str, prize_in: PrizeCreate) -> PrizeResponse:
        hackathon = self.repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{hackathon_id}' not found")
        prize = self.repo.create_prize(hackathon_id, prize_in)
        return PrizeResponse.model_validate(prize)

    def update_prize(self, hackathon_id: str, prize_id: str, prize_in: PrizeUpdate) -> PrizeResponse:
        hackathon = self.repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{hackathon_id}' not found")
        prize = self.repo.get_prize_by_id(prize_id)
        if not prize or prize.hackathon_id != hackathon_id:
            raise NotFoundException(f"Prize '{prize_id}' not found")
        updated = self.repo.update_prize(prize, prize_in)
        return PrizeResponse.model_validate(updated)

    def delete_prize(self, hackathon_id: str, prize_id: str):
        hackathon = self.repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{hackathon_id}' not found")
        prize = self.repo.get_prize_by_id(prize_id)
        if not prize or prize.hackathon_id != hackathon_id:
            raise NotFoundException(f"Prize '{prize_id}' not found")
        self.repo.delete_prize(prize)
