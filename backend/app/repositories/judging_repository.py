import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.judge import Judge
from app.models.judge_assignment import JudgeAssignment
from app.models.submission import Submission
from app.models.review import Review
from app.models.score import Score
from app.schemas.judging import ReviewCreate
from app.utils.enums import ReviewStatus, AssignmentStatus


class JudgingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_judge_by_id(self, judge_id: str) -> Optional[Judge]:
        return self.db.query(Judge).filter(Judge.id == judge_id).first()

    def get_judge_by_user_and_hackathon(self, user_id: str, hackathon_id: str) -> Optional[Judge]:
        return self.db.query(Judge).filter(
            Judge.user_id == user_id,
            Judge.hackathon_id == hackathon_id
        ).first()

    def create_assignment(self, judge_id: str, submission_id: str, assignment_round: int = 1) -> JudgeAssignment:
        assignment_id = f"asgn_{uuid.uuid4().hex[:8]}"
        assignment = JudgeAssignment(
            id=assignment_id,
            judge_id=judge_id,
            submission_id=submission_id,
            status=AssignmentStatus.ASSIGNED,
            assignment_round=assignment_round
        )
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def get_assignment(self, judge_id: str, submission_id: str) -> Optional[JudgeAssignment]:
        return self.db.query(JudgeAssignment).filter(
            JudgeAssignment.judge_id == judge_id,
            JudgeAssignment.submission_id == submission_id
        ).first()

    def get_assignment_by_id(self, assignment_id: str) -> Optional[JudgeAssignment]:
        return self.db.query(JudgeAssignment).filter(JudgeAssignment.id == assignment_id).first()

    def delete_assignment(self, assignment_id: str) -> bool:
        asgn = self.get_assignment_by_id(assignment_id)
        if asgn:
            self.db.delete(asgn)
            self.db.commit()
            return True
        return False

    def list_assignments_for_judge(self, judge_id: str) -> List[JudgeAssignment]:
        return (
            self.db.query(JudgeAssignment)
            .options(joinedload(JudgeAssignment.submission))
            .filter(JudgeAssignment.judge_id == judge_id)
            .all()
        )

    def list_assignments_by_hackathon(self, hackathon_id: str) -> List[JudgeAssignment]:
        return (
            self.db.query(JudgeAssignment)
            .join(Submission, JudgeAssignment.submission_id == Submission.id)
            .filter(Submission.hackathon_id == hackathon_id)
            .all()
        )

    def create_review(self, judge_id: str, rev_in: ReviewCreate) -> Review:
        review_id = f"rev_{uuid.uuid4().hex[:8]}"
        review = Review(
            id=review_id,
            assignment_id=rev_in.assignment_id,
            judge_id=judge_id,
            submission_id=rev_in.submission_id,
            status=ReviewStatus.SUBMITTED,
            comment=rev_in.comment,
            submitted_at=datetime.now(timezone.utc)
        )
        self.db.add(review)
        self.db.flush()

        for s in rev_in.scores:
            score_obj = Score(
                id=f"scr_{uuid.uuid4().hex[:8]}",
                review_id=review_id,
                criterion_id=s.criterion_id,
                score=s.score,
                comment=s.comment
            )
            self.db.add(score_obj)

        if rev_in.assignment_id:
            asgn = self.get_assignment_by_id(rev_in.assignment_id)
            if asgn:
                asgn.status = AssignmentStatus.COMPLETED
                asgn.completed_at = datetime.now(timezone.utc)
                self.db.add(asgn)

        self.db.commit()
        self.db.refresh(review)
        return review

    def get_reviews_for_submission(self, submission_id: str) -> List[Review]:
        return self.db.query(Review).filter(Review.submission_id == submission_id).all()
