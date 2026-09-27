import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class SubmissionCheck(Base):
    __tablename__ = "submission_checks"

    id = Column(String, primary_key=True, index=True)
    submission_id = Column(String, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, index=True)
    check_type = Column(String, nullable=False)
    passed = Column(Boolean, default=True, nullable=False)
    detail = Column(Text, nullable=True)
    checked_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    submission = relationship("Submission", back_populates="checks")
