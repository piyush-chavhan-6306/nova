from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.utils.enums import TeamRole, InvitationStatus


class TeamCreate(BaseModel):
    hackathon_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)


class TeamUpdate(BaseModel):
    name: Optional[str] = None


class TeamMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    team_id: str
    user_id: str
    role: TeamRole
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    joined_at: datetime


class TeamInvitationCreate(BaseModel):
    email: EmailStr


class TeamInvitationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    team_id: str
    email: EmailStr
    token: str
    status: InvitationStatus
    expires_at: Optional[datetime] = None
    created_at: datetime


class TeamInvitationAction(BaseModel):
    accept: bool


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    hackathon_id: str
    name: str
    join_code: Optional[str] = None
    created_at: datetime
    members: List[TeamMemberResponse] = []
