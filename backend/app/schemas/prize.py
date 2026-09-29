from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class PrizeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    value: Optional[str] = None

class PrizeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    value: Optional[str] = None

class PrizeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    hackathon_id: str
    name: str
    description: Optional[str] = None
    value: Optional[str] = None
