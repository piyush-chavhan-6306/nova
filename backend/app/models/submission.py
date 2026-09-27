import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import SubmissionStatus


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String, primary_key=True, index=True)
    hackathon_id = Column(String, ForeignKey("hackathons.id", ondelete="CASCADE"), nullable=False, index=True)
    team_id = Column(String, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    track_id = Column(String, ForeignKey("tracks.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String, nullable=False, index=True)
    summary = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    repo_url = Column(String, nullable=True)
    demo_url = Column(String, nullable=True)
    status = Column(SQLEnum(SubmissionStatus), default=SubmissionStatus.DRAFT, nullable=False)
    submitted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    hackathon = relationship("Hackathon", back_populates="submissions")
    team = relationship("Team", back_populates="submission")
    track = relationship("Track", back_populates="submissions")
    checks = relationship("SubmissionCheck", back_populates="submission", cascade="all, delete-orphan")
    judge_assignments = relationship("JudgeAssignment", back_populates="submission", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="submission", cascade="all, delete-orphan")
    result = relationship("Result", back_populates="submission", uselist=False, cascade="all, delete-orphan")
