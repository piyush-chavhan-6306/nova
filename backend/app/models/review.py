import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import ReviewStatus


class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, index=True)
    assignment_id = Column(String, ForeignKey("judge_assignments.id", ondelete="SET NULL"), nullable=True, index=True)
    judge_id = Column(String, ForeignKey("judges.id", ondelete="CASCADE"), nullable=False, index=True)
    submission_id = Column(String, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(SQLEnum(ReviewStatus), default=ReviewStatus.IN_PROGRESS, nullable=False)
    comment = Column(Text, nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    assignment = relationship("JudgeAssignment", back_populates="review")
    judge = relationship("Judge", back_populates="reviews")
    submission = relationship("Submission", back_populates="reviews")
    scores = relationship("Score", back_populates="review", cascade="all, delete-orphan")
