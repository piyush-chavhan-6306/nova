from typing import List
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, ForbiddenException, NotFoundException
from app.repositories.calibration_repository import CalibrationRepository
from app.repositories.judging_repository import JudgingRepository
from app.repositories.submission_repository import SubmissionRepository
from app.schemas.calibration import (
    CalibrationSetCreate, CalibrationProjectCreate, CalibrationResultCreate,
    CalibrationSetResponse, CalibrationProjectResponse, CalibrationResultResponse, CalibrationSummaryResponse
)
from app.utils.enums import UserRole
from app.core.dependencies import UserIdentity


class CalibrationService:
    def __init__(self, db: Session):
        self.db = db
        self.cal_repo = CalibrationRepository(db)
        self.judging_repo = JudgingRepository(db)
        self.sub_repo = SubmissionRepository(db)

    def create_set(self, hackathon_id: str, set_in: CalibrationSetCreate, current_user: UserIdentity) -> CalibrationSetResponse:
        if current_user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            raise ForbiddenException("Only organizers or admins can create calibration sets")
        cs = self.cal_repo.create_set(hackathon_id, set_in)
        return CalibrationSetResponse.model_validate(cs)

    def list_sets(self, hackathon_id: str) -> List[CalibrationSetResponse]:
        sets = self.cal_repo.list_sets_by_hackathon(hackathon_id)
        return [CalibrationSetResponse.model_validate(s) for s in sets]

    def add_project(self, set_id: str, proj_in: CalibrationProjectCreate, current_user: UserIdentity) -> CalibrationProjectResponse:
        if current_user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            raise ForbiddenException("Only organizers or admins can add projects to a calibration set")
        cs = self.cal_repo.get_set_by_id(set_id)
        if not cs:
            raise NotFoundException("CalibrationSet", set_id)
        sub = self.sub_repo.get_by_id(proj_in.submission_id)
        if not sub:
            raise NotFoundException("Submission", proj_in.submission_id)
        cp = self.cal_repo.add_project(set_id, proj_in)
        return CalibrationProjectResponse.model_validate(cp)

    def record_result(self, res_in: CalibrationResultCreate, current_user: UserIdentity) -> CalibrationResultResponse:
        cs = self.cal_repo.get_set_by_id(res_in.calibration_set_id)
        if not cs:
            raise NotFoundException("CalibrationSet", res_in.calibration_set_id)

        judge = self.judging_repo.get_judge_by_user_and_hackathon(current_user.id, cs.hackathon_id)
        if not judge:
            raise ForbiddenException("You are not registered as a judge for this hackathon")

        cp = self.cal_repo.get_project(res_in.calibration_set_id, res_in.submission_id)
        if not cp:
            raise NotFoundException("CalibrationProject", f"{res_in.calibration_set_id}:{res_in.submission_id}")

        deviation = abs(res_in.score - cp.expected_score)
        cr = self.cal_repo.create_result(judge.id, res_in, deviation)
        return CalibrationResultResponse.model_validate(cr)

    def get_judge_calibration(self, current_user: UserIdentity, hackathon_id: str) -> CalibrationSummaryResponse:
        judge = self.judging_repo.get_judge_by_user_and_hackathon(current_user.id, hackathon_id)
        if not judge:
            return CalibrationSummaryResponse(judge_id=current_user.id, total_calibrated=0, average_deviation=0.0)

        results = self.cal_repo.list_results_by_judge(judge.id)
        if not results:
            return CalibrationSummaryResponse(judge_id=judge.id, total_calibrated=0, average_deviation=0.0)

        avg_dev = sum(r.deviation for r in results) / len(results)
        return CalibrationSummaryResponse(
            judge_id=judge.id,
            total_calibrated=len(results),
            average_deviation=round(avg_dev, 2)
        )

    def get_hackathon_calibration(self, hackathon_id: str, current_user: UserIdentity) -> List[CalibrationResultResponse]:
        if current_user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            raise ForbiddenException("Only organizers or admins can view overall calibration data")
        results = self.cal_repo.list_results_by_hackathon(hackathon_id)
        return [CalibrationResultResponse.model_validate(r) for r in results]
