from typing import List
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, ForbiddenException, NotFoundException
from app.repositories.judge_conflict_repository import JudgeConflictRepository
from app.repositories.judging_repository import JudgingRepository
from app.repositories.submission_repository import SubmissionRepository
from app.schemas.judge_conflict import ConflictDeclareCreate, ConflictResponse
from app.utils.enums import UserRole
from app.core.dependencies import UserIdentity
from app.models.judge import Judge


class JudgeConflictService:
    def __init__(self, db: Session):
        self.db = db
        self.conflict_repo = JudgeConflictRepository(db)
        self.judging_repo = JudgingRepository(db)
        self.sub_repo = SubmissionRepository(db)

    def declare_conflict(self, create_in: ConflictDeclareCreate, current_user: UserIdentity) -> ConflictResponse:
        sub = self.sub_repo.get_by_id(create_in.submission_id)
        if not sub:
            raise NotFoundException("Submission", create_in.submission_id)

        judge = self.judging_repo.get_judge_by_user_and_hackathon(current_user.id, sub.hackathon_id)
        if not judge:
            raise ForbiddenException("You are not registered as a judge for this hackathon")

        if self.conflict_repo.has_active_conflict(judge.id, create_in.submission_id):
            raise BadRequestException("A conflict is already active for this judge and submission")

        conflict = self.conflict_repo.declare_conflict(judge.id, create_in)

        # Cancel any existing assignment for this judge & submission
        assignments = self.judging_repo.list_assignments_for_judge(judge.id)
        for a in assignments:
            if a.submission_id == create_in.submission_id:
                self.judging_repo.delete_assignment(a.id)

        return ConflictResponse.model_validate(conflict)

    def list_my_conflicts(self, current_user: UserIdentity) -> List[ConflictResponse]:
        judges = self.db.query(Judge).filter(Judge.user_id == current_user.id).all()
        conflicts = []
        for j in judges:
            conflicts.extend(self.conflict_repo.list_by_judge(j.id))
        return [ConflictResponse.model_validate(c) for c in conflicts]

    def list_hackathon_conflicts(self, hackathon_id: str, current_user: UserIdentity) -> List[ConflictResponse]:
        if current_user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            raise ForbiddenException("Only organizers or admins can view all conflicts")
        conflicts = self.conflict_repo.list_by_hackathon(hackathon_id)
        return [ConflictResponse.model_validate(c) for c in conflicts]

    def resolve_conflict(self, conflict_id: str, action: str, current_user: UserIdentity) -> ConflictResponse:
        if current_user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            raise ForbiddenException("Only organizers or admins can resolve conflicts")

        conflict = self.conflict_repo.get_by_id(conflict_id)
        if not conflict:
            raise NotFoundException("JudgeConflict", conflict_id)

        status_map = {
            "resolve": "RESOLVED",
            "approve": "APPROVED",
            "reject": "REJECTED"
        }
        new_status = status_map.get(action.lower(), "RESOLVED")

        updated = self.conflict_repo.update_status(conflict, new_status, current_user.id)
        return ConflictResponse.model_validate(updated)
