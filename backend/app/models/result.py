import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(String, primary_key=True, index=True)
    hackathon_id = Column(String, ForeignKey("hackathons.id", ondelete="CASCADE"), nullable=False, index=True)
    submission_id = Column(String, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    raw_score = Column(Float, nullable=False, default=0.0)
    final_score = Column(Float, nullable=False, default=0.0)
    rank = Column(Integer, nullable=True)
    is_published = Column(Boolean, default=False, nullable=False)
    calculated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    hackathon = relationship("Hackathon", back_populates="results")
    submission = relationship("Submission", back_populates="result")
