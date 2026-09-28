import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class JudgeConflict(Base):
    __tablename__ = "judge_conflicts"

    id = Column(String, primary_key=True, index=True)
    judge_id = Column(String, ForeignKey("judges.id", ondelete="CASCADE"), nullable=False, index=True)
    submission_id = Column(String, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, index=True)
    reason = Column(Text, nullable=True)
    status = Column(String, default="DECLARED", nullable=False, index=True)  # DECLARED, APPROVED, REJECTED, RESOLVED
    reported_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    judge = relationship("Judge")
    submission = relationship("Submission")
    resolver = relationship("User")
