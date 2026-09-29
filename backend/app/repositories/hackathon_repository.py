import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.hackathon import Hackathon
from app.models.track import Track
from app.models.prize import Prize
from app.schemas.hackathon import HackathonCreate, HackathonUpdate
from app.schemas.track import TrackCreate, TrackUpdate
from app.schemas.prize import PrizeCreate, PrizeUpdate


class HackathonRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, hackathon_id: str) -> Optional[Hackathon]:
        return self.db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()

    def list_hackathons(self, skip: int = 0, limit: int = 100, search: Optional[str] = None, status: Optional[str] = None) -> List[Hackathon]:
        query = self.db.query(Hackathon)
        if search:
            pattern = f"%{search}%"
            query = query.filter((Hackathon.name.ilike(pattern)) | (Hackathon.description.ilike(pattern)))
        if status:
            query = query.filter(Hackathon.status == status)
        return query.offset(skip).limit(limit).all()

    def count_hackathons(self) -> int:
        return self.db.query(Hackathon).count()

    def create(self, hackathon_in: HackathonCreate, creator_id: Optional[str] = None) -> Hackathon:
        hack_id = f"hack_{uuid.uuid4().hex[:8]}"
        organizer = creator_id or hackathon_in.organizer_id
        hackathon = Hackathon(
            id=hack_id,
            name=hackathon_in.name,
            description=hackathon_in.description,
            registration_start=hackathon_in.registration_start,
            registration_end=hackathon_in.registration_end,
            submissions_start=hackathon_in.submissions_start,
            submissions_close=hackathon_in.submissions_close,
            status=hackathon_in.status,
            max_team_size=hackathon_in.max_team_size,
            min_team_size=hackathon_in.min_team_size,
            payment_required=hackathon_in.payment_required,
            registration_fee=hackathon_in.registration_fee,
            currency=hackathon_in.currency,
            organizer_id=organizer,
        )
        self.db.add(hackathon)
        self.db.commit()
        self.db.refresh(hackathon)
        return hackathon

    def update(self, hackathon: Hackathon, hackathon_in: HackathonUpdate) -> Hackathon:
        update_data = hackathon_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(hackathon, field, value)
        self.db.add(hackathon)
        self.db.commit()
        self.db.refresh(hackathon)
        return hackathon

    # Track operations
    def get_track_by_id(self, track_id: str) -> Optional[Track]:
        return self.db.query(Track).filter(Track.id == track_id).first()

    def list_tracks_for_hackathon(self, hackathon_id: str) -> List[Track]:
        return self.db.query(Track).filter(Track.hackathon_id == hackathon_id).all()

    def create_track(self, hackathon_id: str, track_in: TrackCreate) -> Track:
        track_id = f"trk_{uuid.uuid4().hex[:8]}"
        track = Track(
            id=track_id,
            hackathon_id=hackathon_id,
            name=track_in.name,
            description=track_in.description,
        )
        self.db.add(track)
        self.db.commit()
        self.db.refresh(track)
        return track

    def update_track(self, track: Track, track_in: TrackUpdate) -> Track:
        update_data = track_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(track, field, value)
        self.db.add(track)
        self.db.commit()
        self.db.refresh(track)
        return track

    # Prize operations
    def get_prize_by_id(self, prize_id: str) -> Optional[Prize]:
        return self.db.query(Prize).filter(Prize.id == prize_id).first()

    def list_prizes_for_hackathon(self, hackathon_id: str) -> List[Prize]:
        return self.db.query(Prize).filter(Prize.hackathon_id == hackathon_id).all()

    def create_prize(self, hackathon_id: str, prize_in: PrizeCreate) -> Prize:
        prize_id = f"prz_{uuid.uuid4().hex[:8]}"
        prize = Prize(
            id=prize_id,
            hackathon_id=hackathon_id,
            name=prize_in.name,
            description=prize_in.description,
            value=prize_in.value,
        )
        self.db.add(prize)
        self.db.commit()
        self.db.refresh(prize)
        return prize

    def update_prize(self, prize: Prize, prize_in: PrizeUpdate) -> Prize:
        update_data = prize_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(prize, field, value)
        self.db.add(prize)
        self.db.commit()
        self.db.refresh(prize)
        return prize

    def delete_prize(self, prize: Prize) -> None:
        self.db.delete(prize)
        self.db.commit()
