import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import AssignmentStatus


class JudgeAssignment(Base):
    __tablename__ = "judge_assignments"

    id = Column(String, primary_key=True, index=True)
    judge_id = Column(String, ForeignKey("judges.id", ondelete="CASCADE"), nullable=False, index=True)
    submission_id = Column(String, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = Column(SQLEnum(AssignmentStatus), default=AssignmentStatus.ASSIGNED, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    assignment_round = Column(Integer, default=1, nullable=False)

    # Relationships
    judge = relationship("Judge", back_populates="assignments")
    submission = relationship("Submission", back_populates="judge_assignments")
    review = relationship("Review", back_populates="assignment", uselist=False, cascade="all, delete-orphan")
