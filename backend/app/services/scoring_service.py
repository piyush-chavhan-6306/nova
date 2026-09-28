import csv
import io
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.submission import Submission
from app.models.review import Review
from app.models.score import Score
from app.models.hackathon import Hackathon
from app.repositories.result_repository import ResultRepository
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.audit_repository import AuditRepository
from app.schemas.result import ResultResponse, LeaderboardResponse
from app.utils.enums import ReviewStatus, UserRole
from app.core.exceptions import ForbiddenException, NotFoundException, BadRequestException
from app.core.dependencies import UserIdentity


class ScoringService:
    def __init__(self, db: Session):
        self.db = db
        self.result_repo = ResultRepository(db)
        self.sub_repo = SubmissionRepository(db)
        self.audit_repo = AuditRepository(db)

    def calculate_leaderboard(self, hackathon_id: str, current_user: Optional[UserIdentity] = None) -> LeaderboardResponse:
        hack = self.db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
        if not hack:
            raise NotFoundException("Hackathon", hackathon_id)

        if hack.results_status == "LOCKED":
            raise ForbiddenException("Results for this hackathon are locked")

        submissions = (
            self.db.query(Submission)
            .options(
                joinedload(Submission.team),
                joinedload(Submission.track),
                joinedload(Submission.reviews).joinedload(Review.scores)
            )
            .filter(Submission.hackathon_id == hackathon_id)
            .all()
        )

        computed = []
        for sub in submissions:
            # Gather completed reviews
            valid_reviews = [r for r in sub.reviews if r.status == ReviewStatus.SUBMITTED]
            if not valid_reviews:
                avg_score = 0.0
            else:
                review_scores = []
                for rev in valid_reviews:
                    if rev.scores:
                        r_avg = sum(s.score for s in rev.scores) / len(rev.scores)
                    else:
                        r_avg = 0.0
                    review_scores.append(r_avg)
                avg_score = sum(review_scores) / len(review_scores) if review_scores else 0.0

            computed.append({
                "submission": sub,
                "score": round(avg_score, 2)
            })

        # Sort descending by score
        computed.sort(key=lambda x: x["score"], reverse=True)

        # Upsert results and build response objects
        result_responses = []
        for index, item in enumerate(computed, start=1):
            sub = item["submission"]
            score = item["score"]

            res_entry = self.result_repo.upsert_result(
                hackathon_id=hackathon_id,
                submission_id=sub.id,
                raw_score=score,
                final_score=score,
                rank=index,
                is_published=True
            )

            resp = ResultResponse(
                id=res_entry.id,
                hackathon_id=hackathon_id,
                submission_id=sub.id,
                title=sub.title,
                team_name=sub.team.name if sub.team else None,
                track_name=sub.track.name if sub.track else None,
                raw_score=score,
                final_score=score,
                rank=index,
                is_published=True,
                calculated_at=res_entry.calculated_at
            )
            result_responses.append(resp)

        hack.results_status = "CALCULATED"
        self.db.commit()

        self.audit_repo.log_action(
            action="RESULT_CALCULATED",
            user_id=current_user.id if current_user else None,
            hackathon_id=hackathon_id,
            target_type="hackathon",
            target_id=hackathon_id,
            details="Leaderboard calculated"
        )

        return LeaderboardResponse(
            hackathon_id=hackathon_id,
            total_submissions=len(result_responses),
            results=result_responses
        )

    def transition_result_status(self, hackathon_id: str, new_status: str, current_user: UserIdentity) -> LeaderboardResponse:
        if current_user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            raise ForbiddenException("Only organizers or admins can change result status")

        hack = self.db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
        if not hack:
            raise NotFoundException("Hackathon", hackathon_id)

        if hack.results_status == "LOCKED" and new_status != "LOCKED":
            raise ForbiddenException("Results are locked and cannot be modified")

        valid_statuses = ["DRAFT", "CALCULATED", "UNDER_REVIEW", "APPROVED", "PUBLISHED", "LOCKED"]
        if new_status not in valid_statuses:
            raise BadRequestException(f"Invalid status {new_status}")

        hack.results_status = new_status
        self.db.commit()

        self.audit_repo.log_action(
            action=f"RESULT_{new_status}",
            user_id=current_user.id,
            hackathon_id=hackathon_id,
            target_type="hackathon",
            target_id=hackathon_id,
            details=f"Result status transitioned to {new_status}"
        )

        return self.get_leaderboard(hackathon_id)

    def get_leaderboard(self, hackathon_id: str) -> LeaderboardResponse:
        results = self.result_repo.list_results(hackathon_id)
        if not results:
            return self.calculate_leaderboard(hackathon_id)

        responses = []
        for r in results:
            sub = r.submission
            resp = ResultResponse(
                id=r.id,
                hackathon_id=hackathon_id,
                submission_id=r.submission_id,
                title=sub.title if sub else None,
                team_name=sub.team.name if sub and sub.team else None,
                track_name=sub.track.name if sub and sub.track else None,
                raw_score=r.raw_score,
                final_score=r.final_score,
                rank=r.rank,
                is_published=r.is_published,
                calculated_at=r.calculated_at
            )
            responses.append(resp)

        return LeaderboardResponse(
            hackathon_id=hackathon_id,
            total_submissions=len(responses),
            results=responses
        )

    def export_csv(self, hackathon_id: str) -> str:
        leaderboard = self.get_leaderboard(hackathon_id)
        output = io.StringIO()
        writer = csv.writer(output)

        # Header row
        writer.writerow(["Rank", "Submission ID", "Title", "Team Name", "Track Name", "Final Score"])

        for r in leaderboard.results:
            writer.writerow([
                r.rank,
                r.submission_id,
                r.title or "",
                r.team_name or "",
                r.track_name or "",
                r.final_score
            ])

        return output.getvalue()
