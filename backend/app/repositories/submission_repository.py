import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.submission import Submission
from app.models.team import Team
from app.models.track import Track
from app.schemas.submission import SubmissionCreate, SubmissionUpdate
from app.utils.enums import SubmissionStatus


class SubmissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, submission_id: str) -> Optional[Submission]:
        return (
            self.db.query(Submission)
            .options(joinedload(Submission.team), joinedload(Submission.track))
            .filter(Submission.id == submission_id)
            .first()
        )

    def get_by_team_id(self, team_id: str) -> Optional[Submission]:
        return (
            self.db.query(Submission)
            .options(joinedload(Submission.team), joinedload(Submission.track))
            .filter(Submission.team_id == team_id)
            .first()
        )

    def list_by_hackathon(self, hackathon_id: str) -> List[Submission]:
        return (
            self.db.query(Submission)
            .options(joinedload(Submission.team), joinedload(Submission.track))
            .filter(Submission.hackathon_id == hackathon_id)
            .all()
        )

    def create(self, sub_in: SubmissionCreate) -> Submission:
        sub_id = f"sub_{uuid.uuid4().hex[:8]}"
        initial_status = SubmissionStatus.DRAFT if sub_in.is_draft else SubmissionStatus.SUBMITTED
        submitted_at = None if sub_in.is_draft else datetime.now(timezone.utc)

        submission = Submission(
            id=sub_id,
            hackathon_id=sub_in.hackathon_id,
            team_id=sub_in.team_id,
            track_id=sub_in.track_id,
            title=sub_in.title,
            summary=sub_in.summary,
            description=sub_in.description,
            repo_url=sub_in.repo_url,
            demo_url=sub_in.demo_url,
            status=initial_status,
            submitted_at=submitted_at,
        )
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return self.get_by_id(sub_id)

    def update(self, submission: Submission, sub_in: SubmissionUpdate) -> Submission:
        update_data = sub_in.model_dump(exclude_unset=True)
        is_draft = update_data.pop("is_draft", None)

        for field, value in update_data.items():
            setattr(submission, field, value)

        if is_draft is not None:
            if is_draft:
                submission.status = SubmissionStatus.DRAFT
            else:
                submission.status = SubmissionStatus.SUBMITTED
                submission.submitted_at = datetime.now(timezone.utc)

        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return self.get_by_id(submission.id)

    def list_gallery_submissions(self, hackathon_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Submission]:
        query = (
            self.db.query(Submission)
            .options(joinedload(Submission.team), joinedload(Submission.track))
            .filter(Submission.status != SubmissionStatus.DRAFT)
        )
        if hackathon_id:
            query = query.filter(Submission.hackathon_id == hackathon_id)
        return query.offset(skip).limit(limit).all()
