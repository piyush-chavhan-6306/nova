import statistics
from typing import List
from sqlalchemy.orm import Session
from app.repositories.judging_repository import JudgingRepository
from app.schemas.score_stats import (
    ScoreStatisticsResponse, JudgeScoreStatisticsResponse,
    OutlierDetectionResponse, OutlierScoreItem
)
from app.models.review import Review
from app.models.submission import Submission
from app.utils.enums import ReviewStatus


class ScoreStatsService:
    def __init__(self, db: Session):
        self.db = db
        self.judging_repo = JudgingRepository(db)

    def _get_review_score(self, review: Review) -> float:
        if not review.scores:
            return 0.0
        return sum(s.score for s in review.scores)

    def get_hackathon_statistics(self, hackathon_id: str) -> ScoreStatisticsResponse:
        reviews = (
            self.db.query(Review)
            .join(Submission, Review.submission_id == Submission.id)
            .filter(Submission.hackathon_id == hackathon_id, Review.status == ReviewStatus.SUBMITTED)
            .all()
        )
        scores = [self._get_review_score(r) for r in reviews if r.scores]
        if not scores:
            return ScoreStatisticsResponse(
                hackathon_id=hackathon_id,
                average=0.0,
                median=0.0,
                minimum=0.0,
                maximum=0.0,
                standard_deviation=0.0,
                score_count=0
            )

        avg = statistics.mean(scores)
        med = statistics.median(scores)
        mn = min(scores)
        mx = max(scores)
        stdev = statistics.stdev(scores) if len(scores) > 1 else 0.0

        return ScoreStatisticsResponse(
            hackathon_id=hackathon_id,
            average=round(avg, 2),
            median=round(med, 2),
            minimum=round(mn, 2),
            maximum=round(mx, 2),
            standard_deviation=round(stdev, 2),
            score_count=len(scores)
        )

    def get_judge_statistics(self, judge_id: str) -> JudgeScoreStatisticsResponse:
        reviews = self.db.query(Review).filter(Review.judge_id == judge_id, Review.status == ReviewStatus.SUBMITTED).all()
        scores = [self._get_review_score(r) for r in reviews if r.scores]
        if not scores:
            return JudgeScoreStatisticsResponse(
                judge_id=judge_id,
                average_score=0.0,
                score_variance=0.0,
                completed_reviews=len(reviews),
                average_deviation=0.0
            )

        avg = statistics.mean(scores)
        variance = statistics.variance(scores) if len(scores) > 1 else 0.0
        devs = [abs(s - avg) for s in scores]
        avg_dev = statistics.mean(devs)

        return JudgeScoreStatisticsResponse(
            judge_id=judge_id,
            average_score=round(avg, 2),
            score_variance=round(variance, 2),
            completed_reviews=len(reviews),
            average_deviation=round(avg_dev, 2)
        )

    def get_score_outliers(self, hackathon_id: str) -> OutlierDetectionResponse:
        reviews = (
            self.db.query(Review)
            .join(Submission, Review.submission_id == Submission.id)
            .filter(Submission.hackathon_id == hackathon_id, Review.status == ReviewStatus.SUBMITTED)
            .all()
        )
        scores = [self._get_review_score(r) for r in reviews if r.scores]
        if len(scores) < 2:
            return OutlierDetectionResponse(hackathon_id=hackathon_id, outliers_count=0, outliers=[])

        mean_val = statistics.mean(scores)
        stdev_val = statistics.stdev(scores)
        threshold = 2.0 * stdev_val

        outliers = []
        for r in reviews:
            rev_score = self._get_review_score(r)
            dev = abs(rev_score - mean_val)
            is_out = dev > threshold
            if is_out:
                outliers.append(OutlierScoreItem(
                    review_id=r.id,
                    submission_id=r.submission_id,
                    judge_id=r.judge_id,
                    total_score=rev_score,
                    mean_score=round(mean_val, 2),
                    deviation=round(dev, 2),
                    is_outlier=True
                ))

        return OutlierDetectionResponse(
            hackathon_id=hackathon_id,
            outliers_count=len(outliers),
            outliers=outliers
        )
