import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.result import Result
from app.models.submission import Submission


class ResultRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_submission_id(self, submission_id: str) -> Optional[Result]:
        return self.db.query(Result).filter(Result.submission_id == submission_id).first()

    def upsert_result(
        self,
        hackathon_id: str,
        submission_id: str,
        raw_score: float,
        final_score: float,
        rank: int,
        is_published: bool = True
    ) -> Result:
        res = self.get_by_submission_id(submission_id)
        if not res:
            res = Result(
                id=f"res_{uuid.uuid4().hex[:8]}",
                hackathon_id=hackathon_id,
                submission_id=submission_id,
                raw_score=raw_score,
                final_score=final_score,
                rank=rank,
                is_published=is_published,
                calculated_at=datetime.now(timezone.utc)
            )
            self.db.add(res)
        else:
            res.raw_score = raw_score
            res.final_score = final_score
            res.rank = rank
            res.is_published = is_published
            res.calculated_at = datetime.now(timezone.utc)
            self.db.add(res)

        self.db.commit()
        self.db.refresh(res)
        return res

    def list_results(self, hackathon_id: str) -> List[Result]:
        return (
            self.db.query(Result)
            .options(
                joinedload(Result.submission).joinedload(Submission.team),
                joinedload(Result.submission).joinedload(Submission.track)
            )
            .filter(Result.hackathon_id == hackathon_id)
            .order_by(Result.rank.asc())
            .all()
        )
