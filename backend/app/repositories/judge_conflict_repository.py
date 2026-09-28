import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.judge_conflict import JudgeConflict
from app.schemas.judge_conflict import ConflictDeclareCreate, ConflictUpdate


class JudgeConflictRepository:
    def __init__(self, db: Session):
        self.db = db

    def declare_conflict(self, judge_id: str, create_in: ConflictDeclareCreate) -> JudgeConflict:
        conflict_id = f"cnf_{uuid.uuid4().hex[:8]}"
        conflict = JudgeConflict(
            id=conflict_id,
            judge_id=judge_id,
            submission_id=create_in.submission_id,
            reason=create_in.reason,
            status="DECLARED",
            reported_at=datetime.now(timezone.utc)
        )
        self.db.add(conflict)
        self.db.commit()
        self.db.refresh(conflict)
        return conflict

    def get_by_id(self, conflict_id: str) -> Optional[JudgeConflict]:
        return self.db.query(JudgeConflict).filter(JudgeConflict.id == conflict_id).first()

    def list_by_judge(self, judge_id: str) -> List[JudgeConflict]:
        return self.db.query(JudgeConflict).filter(JudgeConflict.judge_id == judge_id).all()

    def list_by_hackathon(self, hackathon_id: str) -> List[JudgeConflict]:
        from app.models.judge import Judge
        return (
            self.db.query(JudgeConflict)
            .join(Judge, JudgeConflict.judge_id == Judge.id)
            .filter(Judge.hackathon_id == hackathon_id)
            .all()
        )

    def update_status(self, conflict: JudgeConflict, status: str, resolver_user_id: str) -> JudgeConflict:
        conflict.status = status
        conflict.resolved_at = datetime.now(timezone.utc)
        conflict.resolved_by = resolver_user_id
        self.db.commit()
        self.db.refresh(conflict)
        return conflict

    def has_active_conflict(self, judge_id: str, submission_id: str) -> bool:
        c = self.db.query(JudgeConflict).filter(
            JudgeConflict.judge_id == judge_id,
            JudgeConflict.submission_id == submission_id,
            JudgeConflict.status.in_(["DECLARED", "APPROVED"])
        ).first()
        return c is not None
