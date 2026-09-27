from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TrackCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None


class TrackUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TrackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    hackathon_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
