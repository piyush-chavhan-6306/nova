import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.judge import Judge
from app.models.judge_assignment import JudgeAssignment
from app.models.submission import Submission
from app.models.review import Review
from app.models.score import Score
from app.models.rubric import Rubric
from app.models.rubric_criterion import RubricCriterion
from app.models.user import User
from app.models.judge_track import JudgeTrack
from app.schemas.judging import ReviewCreate
from app.schemas.judge import JudgeCreate, JudgeUpdate, JudgeTrackCreate
from app.schemas.rubric import RubricCreate, RubricUpdate, RubricCriterionCreate, RubricCriterionUpdate
from app.utils.enums import ReviewStatus, AssignmentStatus, UserRole


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

    # --- Judge Management ---

    def list_judges_for_hackathon(self, hackathon_id: str) -> List[Judge]:
        return self.db.query(Judge).filter(Judge.hackathon_id == hackathon_id).all()

    def create_judge(self, hackathon_id: str, judge_in: JudgeCreate) -> Judge:
        judge_id = f"jdg_{uuid.uuid4().hex[:8]}"
        judge = Judge(
            id=judge_id,
            user_id=judge_in.user_id,
            hackathon_id=hackathon_id,
            title=judge_in.title,
            bio=judge_in.bio
        )
        self.db.add(judge)
        
        user = self.db.query(User).filter(User.id == judge_in.user_id).first()
        if user and user.role != UserRole.ADMIN and user.role != UserRole.ORGANIZER:
            user.role = UserRole.JUDGE
            self.db.add(user)

        self.db.commit()
        self.db.refresh(judge)
        return judge

    def update_judge(self, judge: Judge, judge_in: JudgeUpdate) -> Judge:
        update_data = judge_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(judge, field, value)
        self.db.add(judge)
        self.db.commit()
        self.db.refresh(judge)
        return judge

    def delete_judge(self, judge: Judge) -> None:
        self.db.delete(judge)
        self.db.commit()

    def assign_judge_track(self, judge_id: str, track_in: JudgeTrackCreate) -> JudgeTrack:
        jt_id = f"jt_{uuid.uuid4().hex[:8]}"
        jt = JudgeTrack(
            id=jt_id,
            judge_id=judge_id,
            track_id=track_in.track_id
        )
        self.db.add(jt)
        self.db.commit()
        self.db.refresh(jt)
        return jt

    def remove_judge_track(self, judge_id: str, track_id: str) -> bool:
        jt = self.db.query(JudgeTrack).filter(
            JudgeTrack.judge_id == judge_id,
            JudgeTrack.track_id == track_id
        ).first()
        if jt:
            self.db.delete(jt)
            self.db.commit()
            return True
        return False

    def list_judge_tracks(self, judge_id: str) -> List[JudgeTrack]:
        return self.db.query(JudgeTrack).filter(JudgeTrack.judge_id == judge_id).all()

    # --- Rubric Management ---

    def list_rubrics_for_hackathon(self, hackathon_id: str) -> List[Rubric]:
        return self.db.query(Rubric).filter(Rubric.hackathon_id == hackathon_id).all()

    def get_rubric(self, rubric_id: str) -> Optional[Rubric]:
        return self.db.query(Rubric).filter(Rubric.id == rubric_id).first()

    def create_rubric(self, hackathon_id: str, rubric_in: RubricCreate) -> Rubric:
        r_id = f"rub_{uuid.uuid4().hex[:8]}"
        rubric = Rubric(
            id=r_id,
            hackathon_id=hackathon_id,
            name=rubric_in.name
        )
        self.db.add(rubric)
        self.db.commit()
        self.db.refresh(rubric)
        return rubric

    def update_rubric(self, rubric: Rubric, rubric_in: RubricUpdate) -> Rubric:
        if rubric_in.name is not None:
            rubric.name = rubric_in.name
        self.db.add(rubric)
        self.db.commit()
        self.db.refresh(rubric)
        return rubric

    def delete_rubric(self, rubric: Rubric) -> None:
        self.db.delete(rubric)
        self.db.commit()

    def get_criterion(self, criterion_id: str) -> Optional[RubricCriterion]:
        return self.db.query(RubricCriterion).filter(RubricCriterion.id == criterion_id).first()

    def create_criterion(self, rubric_id: str, crit_in: RubricCriterionCreate) -> RubricCriterion:
        c_id = f"crit_{uuid.uuid4().hex[:8]}"
        crit = RubricCriterion(
            id=c_id,
            rubric_id=rubric_id,
            name=crit_in.name,
            weight=crit_in.weight,
            max_score=crit_in.max_score
        )
        self.db.add(crit)
        self.db.commit()
        self.db.refresh(crit)
        return crit

    def update_criterion(self, crit: RubricCriterion, crit_in: RubricCriterionUpdate) -> RubricCriterion:
        update_data = crit_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(crit, field, value)
        self.db.add(crit)
        self.db.commit()
        self.db.refresh(crit)
        return crit

    def delete_criterion(self, crit: RubricCriterion) -> None:
        self.db.delete(crit)
        self.db.commit()
