from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.utils.enums import HackathonStatus
from app.schemas.track import TrackResponse


class HackathonCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    registration_start: Optional[datetime] = None
    registration_end: Optional[datetime] = None
    submissions_start: Optional[datetime] = None
    submissions_close: Optional[datetime] = None
    status: HackathonStatus = HackathonStatus.DRAFT
    max_team_size: int = Field(default=4, ge=1, le=10)
    min_team_size: int = Field(default=1, ge=1)
    payment_required: bool = False
    registration_fee: float = 0.0
    currency: str = "USD"


class HackathonUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    registration_start: Optional[datetime] = None
    registration_end: Optional[datetime] = None
    submissions_start: Optional[datetime] = None
    submissions_close: Optional[datetime] = None
    status: Optional[HackathonStatus] = None
    max_team_size: Optional[int] = Field(default=None, ge=1, le=10)
    min_team_size: Optional[int] = Field(default=None, ge=1)
    payment_required: Optional[bool] = None
    registration_fee: Optional[float] = None
    currency: Optional[str] = None


class HackathonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: Optional[str] = None
    registration_start: Optional[datetime] = None
    registration_end: Optional[datetime] = None
    submissions_start: Optional[datetime] = None
    submissions_close: Optional[datetime] = None
    status: HackathonStatus
    min_team_size: int
    max_team_size: int
    payment_required: bool
    registration_fee: float
    currency: str
    created_at: datetime


class HackathonDetailResponse(HackathonResponse):
    tracks: List[TrackResponse] = []
