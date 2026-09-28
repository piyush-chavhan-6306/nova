from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class CalibrationSetCreate(BaseModel):
    name: str


class CalibrationProjectCreate(BaseModel):
    submission_id: str
    expected_score: float


class CalibrationResultCreate(BaseModel):
    calibration_set_id: str
    submission_id: str
    score: float


class CalibrationProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    calibration_set_id: str
    submission_id: str
    expected_score: float
    created_at: datetime


class CalibrationSetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    hackathon_id: str
    name: str
    status: str
    created_at: datetime
    projects: List[CalibrationProjectResponse] = []


class CalibrationResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    calibration_set_id: str
    judge_id: str
    submission_id: str
    score: float
    deviation: float
    completed_at: datetime


class CalibrationSummaryResponse(BaseModel):
    judge_id: str
    total_calibrated: int
    average_deviation: float
