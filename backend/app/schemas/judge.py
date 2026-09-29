from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class JudgeCreate(BaseModel):
    user_id: str
    title: Optional[str] = None
    bio: Optional[str] = None

class JudgeUpdate(BaseModel):
    title: Optional[str] = None
    bio: Optional[str] = None

class JudgeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    hackathon_id: str
    title: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime

class JudgeTrackCreate(BaseModel):
    track_id: str

class JudgeTrackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    judge_id: str
    track_id: str
