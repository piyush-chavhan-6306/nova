from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from app.utils.enums import SubmissionStatus


class SubmissionCreate(BaseModel):
    hackathon_id: str = Field(..., min_length=1)
    team_id: str = Field(..., min_length=1)
    track_id: Optional[str] = None
    title: str = Field(..., min_length=1)
    summary: Optional[str] = None
    description: Optional[str] = None
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    is_draft: bool = False


class SubmissionUpdate(BaseModel):
    track_id: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    is_draft: Optional[bool] = None


class SubmissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    hackathon_id: str
    team_id: str
    track_id: Optional[str] = None
    title: str
    summary: Optional[str] = None
    description: Optional[str] = None
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    status: SubmissionStatus
    submitted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class GalleryProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    hackathon_id: str
    team_id: str
    track_id: Optional[str] = None
    title: str
    summary: Optional[str] = None
    description: Optional[str] = None
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    status: SubmissionStatus
    team_name: Optional[str] = None
    track_name: Optional[str] = None
    submitted_at: Optional[datetime] = None
