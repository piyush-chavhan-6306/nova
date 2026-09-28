from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, ForbiddenException, NotFoundException
from app.repositories.pairwise_repository import PairwiseRepository
from app.repositories.judging_repository import JudgingRepository
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.team_repository import TeamRepository
from app.schemas.pairwise import (
    PairwiseEvaluationCreate, PairwiseEvaluationUpdate,
    PairwiseEvaluationResponse, PairwiseProgressResponse
)
from app.utils.enums import PairwiseStatus, UserRole
from app.core.dependencies import UserIdentity


class PairwiseService:
    def __init__(self, db: Session):
        self.db = db
        self.pairwise_repo = PairwiseRepository(db)
        self.judging_repo = JudgingRepository(db)
        self.sub_repo = SubmissionRepository(db)
        self.team_repo = TeamRepository(db)

    def _validate_judge_and_peer_isolation(self, judge_user_id: str, sub_a_id: str, sub_b_id: str):
        if sub_a_id == sub_b_id:
            raise BadRequestException("A submission cannot be compared with itself")

        sub_a = self.sub_repo.get_by_id(sub_a_id)
        sub_b = self.sub_repo.get_by_id(sub_b_id)
        if not sub_a or not sub_b:
            raise NotFoundException("Submission", f"{sub_a_id} or {sub_b_id}")

        # Peer isolation checks
        member_a = self.team_repo.get_member(sub_a.team_id, judge_user_id)
        member_b = self.team_repo.get_member(sub_b.team_id, judge_user_id)
        if member_a or member_b:
            raise ForbiddenException("Judge cannot evaluate their own team's project in pairwise comparison")

    def create_evaluation(self, create_in: PairwiseEvaluationCreate, current_user: UserIdentity) -> PairwiseEvaluationResponse:
        judge = None
        if create_in.judge_id:
            judge = self.judging_repo.get_judge_by_id(create_in.judge_id)
        else:
            judge = self.judging_repo.get_judge_by_user_and_hackathon(current_user.id, create_in.hackathon_id)

        if not judge:
            raise NotFoundException("Judge", create_in.judge_id or current_user.id)

        self._validate_judge_and_peer_isolation(judge.user_id, create_in.submission_a_id, create_in.submission_b_id)

        existing = self.pairwise_repo.find_existing_pair(judge.id, create_in.submission_a_id, create_in.submission_b_id)
        if existing:
            return PairwiseEvaluationResponse.model_validate(existing)

        pe = self.pairwise_repo.create(create_in.hackathon_id, judge.id, create_in.submission_a_id, create_in.submission_b_id)
        return PairwiseEvaluationResponse.model_validate(pe)

    def get_evaluation(self, eval_id: str, current_user: UserIdentity) -> PairwiseEvaluationResponse:
        pe = self.pairwise_repo.get_by_id(eval_id)
        if not pe:
            raise NotFoundException("PairwiseEvaluation", eval_id)

        # Check permission: judge can access own only unless ORGANIZER/ADMIN
        if current_user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            judge = self.judging_repo.get_judge_by_user_and_hackathon(current_user.id, pe.hackathon_id)
            if not judge or judge.id != pe.judge_id:
                raise ForbiddenException("Access denied to another judge's pairwise evaluation")

        return PairwiseEvaluationResponse.model_validate(pe)

    def update_evaluation(self, eval_id: str, update_in: PairwiseEvaluationUpdate, current_user: UserIdentity) -> PairwiseEvaluationResponse:
        pe = self.pairwise_repo.get_by_id(eval_id)
        if not pe:
            raise NotFoundException("PairwiseEvaluation", eval_id)

        if pe.status in [PairwiseStatus.SUBMITTED, PairwiseStatus.LOCKED]:
            raise BadRequestException("Submitted or locked pairwise evaluations cannot be modified")

        # Check permission
        if current_user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            judge = self.judging_repo.get_judge_by_user_and_hackathon(current_user.id, pe.hackathon_id)
            if not judge or judge.id != pe.judge_id:
                raise ForbiddenException("Access denied to edit another judge's pairwise evaluation")

        if update_in.winner_submission_id and update_in.winner_submission_id not in [pe.submission_a_id, pe.submission_b_id]:
            raise BadRequestException("Winner submission must be one of the compared projects")

        updated = self.pairwise_repo.update(pe, update_in)
        return PairwiseEvaluationResponse.model_validate(updated)

    def submit_evaluation(self, eval_id: str, current_user: UserIdentity) -> PairwiseEvaluationResponse:
        pe = self.pairwise_repo.get_by_id(eval_id)
        if not pe:
            raise NotFoundException("PairwiseEvaluation", eval_id)

        if not pe.winner_submission_id:
            raise BadRequestException("Cannot submit evaluation without declaring a winner submission")

        return self.update_evaluation(eval_id, PairwiseEvaluationUpdate(status=PairwiseStatus.SUBMITTED), current_user)

    def lock_evaluation(self, eval_id: str, current_user: UserIdentity) -> PairwiseEvaluationResponse:
        if current_user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            raise ForbiddenException("Only organizers or admins can lock pairwise evaluations")

        pe = self.pairwise_repo.get_by_id(eval_id)
        if not pe:
            raise NotFoundException("PairwiseEvaluation", eval_id)

        return self.update_evaluation(eval_id, PairwiseEvaluationUpdate(status=PairwiseStatus.LOCKED), current_user)

    def list_my_pairwise_evaluations(self, hackathon_id: str, current_user: UserIdentity) -> List[PairwiseEvaluationResponse]:
        judge = self.judging_repo.get_judge_by_user_and_hackathon(current_user.id, hackathon_id)
        if not judge:
            return []
        evals = self.pairwise_repo.list_by_judge(judge.id)
        return [PairwiseEvaluationResponse.model_validate(e) for e in evals]

    def list_hackathon_pairwise(self, hackathon_id: str, current_user: UserIdentity) -> List[PairwiseEvaluationResponse]:
        if current_user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            raise ForbiddenException("Only organizers or admins can view all pairwise evaluations")
        evals = self.pairwise_repo.list_by_hackathon(hackathon_id)
        return [PairwiseEvaluationResponse.model_validate(e) for e in evals]

    def get_progress(self, hackathon_id: str, current_user: UserIdentity) -> PairwiseProgressResponse:
        evals = self.pairwise_repo.list_by_hackathon(hackathon_id)
        total = len(evals)
        completed = len([e for e in evals if e.status in [PairwiseStatus.SUBMITTED, PairwiseStatus.LOCKED]])
        percentage = (completed / total * 100.0) if total > 0 else 0.0
        return PairwiseProgressResponse(
            total_pairs=total,
            completed_pairs=completed,
            completion_percentage=round(percentage, 2)
        )
