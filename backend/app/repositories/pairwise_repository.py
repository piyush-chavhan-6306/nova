import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.pairwise_evaluation import PairwiseEvaluation
from app.schemas.pairwise import PairwiseEvaluationCreate, PairwiseEvaluationUpdate
from app.utils.enums import PairwiseStatus


class PairwiseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, hackathon_id: str, judge_id: str, sub_a_id: str, sub_b_id: str) -> PairwiseEvaluation:
        eval_id = f"pair_{uuid.uuid4().hex[:8]}"
        pe = PairwiseEvaluation(
            id=eval_id,
            hackathon_id=hackathon_id,
            judge_id=judge_id,
            submission_a_id=sub_a_id,
            submission_b_id=sub_b_id,
            status=PairwiseStatus.ASSIGNED,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(pe)
        self.db.commit()
        self.db.refresh(pe)
        return pe

    def get_by_id(self, eval_id: str) -> Optional[PairwiseEvaluation]:
        return self.db.query(PairwiseEvaluation).filter(PairwiseEvaluation.id == eval_id).first()

    def find_existing_pair(self, judge_id: str, sub_a_id: str, sub_b_id: str) -> Optional[PairwiseEvaluation]:
        return self.db.query(PairwiseEvaluation).filter(
            PairwiseEvaluation.judge_id == judge_id,
            (
                ((PairwiseEvaluation.submission_a_id == sub_a_id) & (PairwiseEvaluation.submission_b_id == sub_b_id)) |
                ((PairwiseEvaluation.submission_a_id == sub_b_id) & (PairwiseEvaluation.submission_b_id == sub_a_id))
            )
        ).first()

    def list_by_judge(self, judge_id: str) -> List[PairwiseEvaluation]:
        return self.db.query(PairwiseEvaluation).filter(PairwiseEvaluation.judge_id == judge_id).all()

    def list_by_hackathon(self, hackathon_id: str) -> List[PairwiseEvaluation]:
        return self.db.query(PairwiseEvaluation).filter(PairwiseEvaluation.hackathon_id == hackathon_id).all()

    def update(self, pe: PairwiseEvaluation, update_in: PairwiseEvaluationUpdate) -> PairwiseEvaluation:
        if update_in.winner_submission_id is not None:
            pe.winner_submission_id = update_in.winner_submission_id
        if update_in.reason is not None:
            pe.reason = update_in.reason
        if update_in.status is not None:
            pe.status = update_in.status
            if update_in.status in [PairwiseStatus.SUBMITTED, PairwiseStatus.LOCKED]:
                pe.completed_at = datetime.now(timezone.utc)
        self.db.add(pe)
        self.db.commit()
        self.db.refresh(pe)
        return pe
