from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, ForbiddenException, NotFoundException, SubmissionClosedException
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.team_repository import TeamRepository
from app.schemas.submission import SubmissionCreate, SubmissionUpdate, SubmissionResponse, GalleryProjectResponse
from app.utils.enums import SubmissionStatus, HackathonStatus, UserRole
from app.core.dependencies import UserIdentity


class SubmissionService:
    def __init__(self, db: Session):
        self.db = db
        self.sub_repo = SubmissionRepository(db)
        self.team_repo = TeamRepository(db)
        self.hack_repo = HackathonRepository(db)

    def _check_event_open_for_submissions(self, hackathon_id: str):
        hackathon = self.hack_repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException("Hackathon", hackathon_id)

        # Check status
        if hackathon.status in [HackathonStatus.SUBMISSIONS_CLOSED, HackathonStatus.CLOSED, HackathonStatus.ARCHIVED]:
            raise SubmissionClosedException("Submissions for this event are closed")

        # Check close timestamp
        if hackathon.submissions_close:
            now_utc = datetime.now(timezone.utc)
            close_time = hackathon.submissions_close
            # If naive datetime, make UTC aware for comparison
            if close_time.tzinfo is None:
                close_time = close_time.replace(tzinfo=timezone.utc)
            if now_utc > close_time:
                raise SubmissionClosedException("Submissions deadline has passed")

    def _build_gallery_response(self, sub, current_user: Optional[UserIdentity] = None) -> GalleryProjectResponse:
        hackathon = self.hack_repo.get_by_id(sub.hackathon_id)
        is_blind = hackathon.blind_review_enabled if hackathon else False
        is_judge = current_user and current_user.role == UserRole.JUDGE

        team_name = sub.team.name if sub.team else None
        track_name = sub.track.name if sub.track else None
        resp = GalleryProjectResponse.model_validate(sub)

        if is_blind and is_judge:
            resp.team_id = "ANONYMOUS"
            resp.team_name = "Anonymous Team"
        else:
            resp.team_name = team_name

        resp.track_name = track_name
        return resp

    def create_submission(self, sub_in: SubmissionCreate, current_user_id: str) -> SubmissionResponse:
        self._check_event_open_for_submissions(sub_in.hackathon_id)

        # Verify user belongs to the team
        team_member = self.team_repo.get_member(sub_in.team_id, current_user_id)
        if not team_member:
            raise ForbiddenException("You must be a member of the team to submit a project")

        # Check if team already has a submission
        existing = self.sub_repo.get_by_team_id(sub_in.team_id)
        if existing:
            raise BadRequestException("Your team has already created a submission for this event")

        submission = self.sub_repo.create(sub_in)
        return SubmissionResponse.model_validate(submission)

    def update_submission(self, submission_id: str, sub_in: SubmissionUpdate, current_user_id: str) -> SubmissionResponse:
        submission = self.sub_repo.get_by_id(submission_id)
        if not submission:
            raise NotFoundException("Submission", submission_id)

        self._check_event_open_for_submissions(submission.hackathon_id)

        # Verify team membership
        team_member = self.team_repo.get_member(submission.team_id, current_user_id)
        if not team_member:
            raise ForbiddenException("You must be a member of the team to update the submission")

        updated = self.sub_repo.update(submission, sub_in)
        return SubmissionResponse.model_validate(updated)

    def get_submission(self, submission_id: str, current_user: Optional[UserIdentity] = None) -> SubmissionResponse:
        submission = self.sub_repo.get_by_id(submission_id)
        if not submission:
            raise NotFoundException("Submission", submission_id)

        resp = SubmissionResponse.model_validate(submission)
        hackathon = self.hack_repo.get_by_id(submission.hackathon_id)
        if hackathon and hackathon.blind_review_enabled:
            if current_user and current_user.role == UserRole.JUDGE:
                resp.team_id = "ANONYMOUS"

        return resp

    def list_gallery_projects(self, hackathon_id: Optional[str] = None, skip: int = 0, limit: int = 100, current_user: Optional[UserIdentity] = None) -> List[GalleryProjectResponse]:
        submissions = self.sub_repo.list_gallery_submissions(hackathon_id=hackathon_id, skip=skip, limit=limit)
        return [self._build_gallery_response(s, current_user) for s in submissions]
