from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.utils.enums import RegistrationStatus


class RegistrationCreate(BaseModel):
    hackathon_id: str


class RegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    hackathon_id: str
    user_id: str
    status: RegistrationStatus
    created_at: datetime
