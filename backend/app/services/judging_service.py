from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, ForbiddenException, NotFoundException
from app.repositories.judging_repository import JudgingRepository
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.team_repository import TeamRepository
from app.schemas.judging import (
    JudgeAssignmentCreate, BatchJudgeAssignmentCreate, JudgeAssignmentResponse,
    ReviewCreate, ReviewResponse
)
from app.models.team_member import TeamMember
from app.models.team import Team
from app.models.judge import Judge
from app.models.judge_track import JudgeTrack
from app.models.submission import Submission


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

        assignment = self.judging_repo.create_assignment(
            assign_in.judge_id,
            assign_in.submission_id,
            assignment_round=assign_in.assignment_round or 1
        )
        return JudgeAssignmentResponse.model_validate(assignment)

    def batch_assign_judges(self, batch_in: BatchJudgeAssignmentCreate) -> List[JudgeAssignmentResponse]:
        """
        Track-aware, workload-balanced batch assignment.
        Excludes judges with conflicts/peer isolation.
        """
        submissions = self.sub_repo.list_by_hackathon(batch_in.hackathon_id)
        judges = self.db.query(Judge).filter(Judge.hackathon_id == batch_in.hackathon_id).all()
        if not submissions or not judges:
            return []

        # Map judges to assigned tracks
        judge_tracks = self.db.query(JudgeTrack).all()
        j_track_map = {}
        for jt in judge_tracks:
            j_track_map.setdefault(jt.judge_id, set()).add(jt.track_id)

        # Workload counter (judge_id -> assignment count)
        workload = {j.id: 0 for j in judges}
        existing_assignments = self.judging_repo.list_assignments_by_hackathon(batch_in.hackathon_id)
        for asgn in existing_assignments:
            if asgn.judge_id in workload:
                workload[asgn.judge_id] += 1

        created_assignments = []
        target = batch_in.target_reviews_per_project or 2

        for sub in submissions:
            # Current assignments for sub
            sub_asgns = [a for a in existing_assignments if a.submission_id == sub.id]
            needed = max(0, target - len(sub_asgns))
            if needed <= 0:
                continue

            # Eligible judges for sub (track match, no peer isolation, not assigned yet)
            already_assigned_judges = {a.judge_id for a in sub_asgns}
            eligible = []

            for j in judges:
                if j.id in already_assigned_judges:
                    continue

                # Track check (if judge has specified tracks, match track_id)
                j_tracks = j_track_map.get(j.id, set())
                if j_tracks and sub.track_id and sub.track_id not in j_tracks:
                    continue

                # Peer isolation check
                try:
                    self._validate_peer_isolation(j.user_id, sub.id)
                    eligible.append(j)
                except ForbiddenException:
                    continue

            # Sort eligible judges by workload (ascending)
            eligible.sort(key=lambda j: workload[j.id])

            # Assign up to 'needed'
            for j in eligible[:needed]:
                asgn = self.judging_repo.create_assignment(j.id, sub.id, assignment_round=batch_in.assignment_round or 1)
                workload[j.id] += 1
                created_assignments.append(JudgeAssignmentResponse.model_validate(asgn))

        return created_assignments

    def delete_assignment(self, assignment_id: str) -> bool:
        asgn = self.judging_repo.get_assignment_by_id(assignment_id)
        if not asgn:
            raise NotFoundException("JudgeAssignment", assignment_id)
        return self.judging_repo.delete_assignment(assignment_id)

    def list_my_assignments(self, current_user_id: str, hackathon_id: str) -> List[JudgeAssignmentResponse]:
        judge = self.judging_repo.get_judge_by_user_and_hackathon(current_user_id, hackathon_id)
        if not judge:
            return []
        assignments = self.judging_repo.list_assignments_for_judge(judge.id)
        return [JudgeAssignmentResponse.model_validate(a) for a in assignments]

    def list_hackathon_assignments(self, hackathon_id: str) -> List[JudgeAssignmentResponse]:
        assignments = self.judging_repo.list_assignments_by_hackathon(hackathon_id)
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
