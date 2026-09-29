from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

class RubricCriterionCreate(BaseModel):
    name: str = Field(..., min_length=1)
    weight: float = Field(default=1.0, gt=0)
    max_score: float = Field(default=5.0, gt=0)

class RubricCriterionUpdate(BaseModel):
    name: Optional[str] = None
    weight: Optional[float] = Field(default=None, gt=0)
    max_score: Optional[float] = Field(default=None, gt=0)

class RubricCriterionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    rubric_id: str
    name: str
    weight: float
    max_score: float
    created_at: datetime

class RubricCreate(BaseModel):
    name: str = Field(..., min_length=1)

class RubricUpdate(BaseModel):
    name: Optional[str] = None

class RubricResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    hackathon_id: str
    name: str
    created_at: datetime

class RubricDetailResponse(RubricResponse):
    criteria: List[RubricCriterionResponse] = []
