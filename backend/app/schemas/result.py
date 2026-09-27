from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class ResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    hackathon_id: str
    submission_id: str
    title: Optional[str] = None
    team_name: Optional[str] = None
    track_name: Optional[str] = None
    raw_score: float
    final_score: float
    rank: Optional[int] = None
    is_published: bool
    calculated_at: datetime


class LeaderboardResponse(BaseModel):
    hackathon_id: str
    total_submissions: int
    results: List[ResultResponse]
