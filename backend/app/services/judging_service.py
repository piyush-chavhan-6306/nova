from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, ForbiddenException, NotFoundException
from app.repositories.judging_repository import JudgingRepository
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.team_repository import TeamRepository
from app.schemas.judging import (
    JudgeAssignmentCreate, JudgeAssignmentResponse,
    ReviewCreate, ReviewResponse
)
from app.models.team_member import TeamMember
from app.models.team import Team


class JudgingService:
    def __init__(self, db: Session):
        self.db = db
        self.judging_repo = JudgingRepository(db)
        self.sub_repo = SubmissionRepository(db)
        self.team_repo = TeamRepository(db)

    def _validate_peer_isolation(self, judge_user_id: str, submission_id: str):
        """
        Enforce T2 Peer Isolation Guard:
        Prevent judges from reviewing projects submitted by their own team or 
        events where they are registered as competing participants.
        """
        submission = self.sub_repo.get_by_id(submission_id)
        if not submission:
            raise NotFoundException("Submission", submission_id)

        # 1. Check if judge user is a member of the submission's team
        team_member = self.team_repo.get_member(submission.team_id, judge_user_id)
        if team_member:
            raise ForbiddenException("Peer isolation guard: Judge cannot review their own team's submission")

        # 2. Check if judge user is a competitor/participant on ANY team in the same hackathon
        competitor_member = (
            self.db.query(TeamMember)
            .join(Team, TeamMember.team_id == Team.id)
            .filter(
                Team.hackathon_id == submission.hackathon_id,
                TeamMember.user_id == judge_user_id
            )
            .first()
        )
        if competitor_member:
            raise ForbiddenException("Peer isolation guard: Judge cannot review submissions in an event where they are competing")

    def assign_judge(self, assign_in: JudgeAssignmentCreate) -> JudgeAssignmentResponse:
        judge = self.judging_repo.get_judge_by_id(assign_in.judge_id)
        if not judge:
            raise NotFoundException("Judge", assign_in.judge_id)

        # Validate peer isolation before assignment
        self._validate_peer_isolation(judge.user_id, assign_in.submission_id)

        existing = self.judging_repo.get_assignment(assign_in.judge_id, assign_in.submission_id)
        if existing:
            return JudgeAssignmentResponse.model_validate(existing)

        assignment = self.judging_repo.create_assignment(assign_in.judge_id, assign_in.submission_id)
        return JudgeAssignmentResponse.model_validate(assignment)

    def list_my_assignments(self, current_user_id: str, hackathon_id: str) -> List[JudgeAssignmentResponse]:
        judge = self.judging_repo.get_judge_by_user_and_hackathon(current_user_id, hackathon_id)
        if not judge:
            return []
        assignments = self.judging_repo.list_assignments_for_judge(judge.id)
        return [JudgeAssignmentResponse.model_validate(a) for a in assignments]

    def submit_review(self, rev_in: ReviewCreate, current_user_id: str) -> ReviewResponse:
        submission = self.sub_repo.get_by_id(rev_in.submission_id)
        if not submission:
            raise NotFoundException("Submission", rev_in.submission_id)

        judge = self.judging_repo.get_judge_by_user_and_hackathon(current_user_id, submission.hackathon_id)
        if not judge:
            raise ForbiddenException("You are not registered as a judge for this hackathon")

        # Validate peer isolation before submitting review
        self._validate_peer_isolation(current_user_id, rev_in.submission_id)

        review = self.judging_repo.create_review(judge.id, rev_in)
        return ReviewResponse.model_validate(review)

    def get_reviews_for_submission(self, submission_id: str) -> List[ReviewResponse]:
        reviews = self.judging_repo.get_reviews_for_submission(submission_id)
        return [ReviewResponse.model_validate(r) for r in reviews]
