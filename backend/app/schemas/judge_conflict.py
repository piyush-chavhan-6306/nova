from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ConflictDeclareCreate(BaseModel):
    submission_id: str
    reason: Optional[str] = None


class ConflictUpdate(BaseModel):
    reason: Optional[str] = None


class ConflictResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    judge_id: str
    submission_id: str
    reason: Optional[str] = None
    status: str
    reported_at: datetime
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
