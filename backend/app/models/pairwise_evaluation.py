import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import PairwiseStatus


class PairwiseEvaluation(Base):
    __tablename__ = "pairwise_evaluations"

    id = Column(String, primary_key=True, index=True)
    hackathon_id = Column(String, ForeignKey("hackathons.id", ondelete="CASCADE"), nullable=False, index=True)
    judge_id = Column(String, ForeignKey("judges.id", ondelete="CASCADE"), nullable=False, index=True)
    submission_a_id = Column(String, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, index=True)
    submission_b_id = Column(String, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, index=True)
    winner_submission_id = Column(String, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=True)
    reason = Column(String, nullable=True)
    status = Column(SQLEnum(PairwiseStatus), default=PairwiseStatus.ASSIGNED, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    hackathon = relationship("Hackathon")
    judge = relationship("Judge")
    submission_a = relationship("Submission", foreign_keys=[submission_a_id])
    submission_b = relationship("Submission", foreign_keys=[submission_b_id])
    winner_submission = relationship("Submission", foreign_keys=[winner_submission_id])
