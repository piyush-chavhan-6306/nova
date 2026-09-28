import statistics
from typing import List
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ForbiddenException
from app.models.judge import Judge
from app.models.judge_assignment import JudgeAssignment
from app.models.review import Review
from app.models.submission import Submission
from app.models.pairwise_evaluation import PairwiseEvaluation
from app.models.calibration import CalibrationResult
from app.schemas.judge_dashboard import JudgeDashboardResponse, HackathonJudgingProgressResponse, JudgeWorkloadItem
from app.utils.enums import AssignmentStatus, ReviewStatus, PairwiseStatus, UserRole
from app.core.dependencies import UserIdentity


class JudgeDashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_judge_dashboard(self, current_user: UserIdentity, hackathon_id: str) -> JudgeDashboardResponse:
        judge = self.db.query(Judge).filter(Judge.user_id == current_user.id, Judge.hackathon_id == hackathon_id).first()
        if not judge:
            return JudgeDashboardResponse(
                judge_id=current_user.id,
                assigned_projects=0,
                completed_reviews=0,
                pending_reviews=0,
                completion_percentage=0.0,
                pairwise_pending=0,
                calibration_status="PENDING",
                average_score=0.0
            )

        assignments = self.db.query(JudgeAssignment).filter(JudgeAssignment.judge_id == judge.id).all()
        assigned_count = len(assignments)

        completed_reviews = (
            self.db.query(Review)
            .filter(Review.judge_id == judge.id, Review.status == ReviewStatus.SUBMITTED)
            .all()
        )
        completed_count = len(completed_reviews)
        pending_count = max(0, assigned_count - completed_count)
        completion_pct = round((completed_count / assigned_count * 100.0), 2) if assigned_count > 0 else 0.0

        pairwise_pending = (
            self.db.query(PairwiseEvaluation)
            .filter(PairwiseEvaluation.judge_id == judge.id, PairwiseEvaluation.status != PairwiseStatus.SUBMITTED)
            .count()
        )

        cal_count = self.db.query(CalibrationResult).filter(CalibrationResult.judge_id == judge.id).count()
        calibration_status = "COMPLETED" if cal_count > 0 else "PENDING"

        scores = []
        for r in completed_reviews:
            if r.scores:
                scores.append(sum(s.score for s in r.scores))
        avg_score = round(statistics.mean(scores), 2) if scores else 0.0

        return JudgeDashboardResponse(
            judge_id=judge.id,
            assigned_projects=assigned_count,
            completed_reviews=completed_count,
            pending_reviews=pending_count,
            completion_percentage=completion_pct,
            pairwise_pending=pairwise_pending,
            calibration_status=calibration_status,
            average_score=avg_score
        )

    def get_hackathon_judging_progress(self, hackathon_id: str) -> HackathonJudgingProgressResponse:
        total_submissions = self.db.query(Submission).filter(Submission.hackathon_id == hackathon_id).count()
        
        assignments = (
            self.db.query(JudgeAssignment)
            .join(Submission, JudgeAssignment.submission_id == Submission.id)
            .filter(Submission.hackathon_id == hackathon_id)
            .all()
        )
        total_assignments = len(assignments)
        completed_assignments = sum(1 for a in assignments if a.status == AssignmentStatus.COMPLETED)
        pending_assignments = max(0, total_assignments - completed_assignments)
        completion_pct = round((completed_assignments / total_assignments * 100.0), 2) if total_assignments > 0 else 0.0

        judges = self.db.query(Judge).filter(Judge.hackathon_id == hackathon_id).all()
        workload = []
        for j in judges:
            j_assigns = [a for a in assignments if a.judge_id == j.id]
            j_tot = len(j_assigns)
            j_comp = sum(1 for a in j_assigns if a.status == AssignmentStatus.COMPLETED)
            j_pct = round((j_comp / j_tot * 100.0), 2) if j_tot > 0 else 0.0
            workload.append(JudgeWorkloadItem(
                judge_id=j.id,
                judge_name=j.user.name if j.user else j.id,
                assigned_count=j_tot,
                completed_count=j_comp,
                completion_percentage=j_pct
            ))

        pairwise_comp = (
            self.db.query(PairwiseEvaluation)
            .filter(PairwiseEvaluation.hackathon_id == hackathon_id, PairwiseEvaluation.status == PairwiseStatus.SUBMITTED)
            .count()
        )

        cal_comp = (
            self.db.query(CalibrationResult)
            .join(Judge, CalibrationResult.judge_id == Judge.id)
            .filter(Judge.hackathon_id == hackathon_id)
            .count()
        )

        return HackathonJudgingProgressResponse(
            hackathon_id=hackathon_id,
            total_submissions=total_submissions,
            total_assignments=total_assignments,
            completed_assignments=completed_assignments,
            pending_assignments=pending_assignments,
            completion_percentage=completion_pct,
            judge_workload=workload,
            pairwise_completed_pairs=pairwise_comp,
            calibration_completed_count=cal_comp
        )
