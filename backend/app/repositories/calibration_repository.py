import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.calibration import CalibrationSet, CalibrationProject, CalibrationResult
from app.schemas.calibration import CalibrationSetCreate, CalibrationProjectCreate, CalibrationResultCreate


class CalibrationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_set(self, hackathon_id: str, set_in: CalibrationSetCreate) -> CalibrationSet:
        cs_id = f"cal_{uuid.uuid4().hex[:8]}"
        cs = CalibrationSet(
            id=cs_id,
            hackathon_id=hackathon_id,
            name=set_in.name,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(cs)
        self.db.commit()
        self.db.refresh(cs)
        return cs

    def get_set_by_id(self, cs_id: str) -> Optional[CalibrationSet]:
        return self.db.query(CalibrationSet).filter(CalibrationSet.id == cs_id).first()

    def list_sets_by_hackathon(self, hackathon_id: str) -> List[CalibrationSet]:
        return self.db.query(CalibrationSet).filter(CalibrationSet.hackathon_id == hackathon_id).all()

    def add_project(self, cs_id: str, proj_in: CalibrationProjectCreate) -> CalibrationProject:
        cp_id = f"cp_{uuid.uuid4().hex[:8]}"
        cp = CalibrationProject(
            id=cp_id,
            calibration_set_id=cs_id,
            submission_id=proj_in.submission_id,
            expected_score=proj_in.expected_score,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(cp)
        self.db.commit()
        self.db.refresh(cp)
        return cp

    def get_project(self, cs_id: str, sub_id: str) -> Optional[CalibrationProject]:
        return self.db.query(CalibrationProject).filter(
            CalibrationProject.calibration_set_id == cs_id,
            CalibrationProject.submission_id == sub_id
        ).first()

    def create_result(self, judge_id: str, res_in: CalibrationResultCreate, deviation: float) -> CalibrationResult:
        cr_id = f"cr_{uuid.uuid4().hex[:8]}"
        cr = CalibrationResult(
            id=cr_id,
            calibration_set_id=res_in.calibration_set_id,
            judge_id=judge_id,
            submission_id=res_in.submission_id,
            score=res_in.score,
            deviation=deviation,
            completed_at=datetime.now(timezone.utc)
        )
        self.db.add(cr)
        self.db.commit()
        self.db.refresh(cr)
        return cr

    def list_results_by_judge(self, judge_id: str) -> List[CalibrationResult]:
        return self.db.query(CalibrationResult).filter(CalibrationResult.judge_id == judge_id).all()

    def list_results_by_hackathon(self, hackathon_id: str) -> List[CalibrationResult]:
        return (
            self.db.query(CalibrationResult)
            .join(CalibrationSet, CalibrationResult.calibration_set_id == CalibrationSet.id)
            .filter(CalibrationSet.hackathon_id == hackathon_id)
            .all()
        )
