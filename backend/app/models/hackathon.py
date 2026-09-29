import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import HackathonStatus


class Hackathon(Base):
    __tablename__ = "hackathons"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    registration_start = Column(DateTime, nullable=True)
    registration_end = Column(DateTime, nullable=True)
    submissions_start = Column(DateTime, nullable=True)
    submissions_close = Column(DateTime, nullable=True, index=True)
    min_team_size = Column(Integer, default=1, nullable=False)
    max_team_size = Column(Integer, default=5, nullable=False)
    payment_required = Column(Boolean, default=False, nullable=False)
    registration_fee = Column(Float, default=0.0, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    blind_review_enabled = Column(Boolean, default=False, nullable=False)
    results_status = Column(String, default="DRAFT", nullable=False)  # DRAFT, CALCULATED, UNDER_REVIEW, APPROVED, PUBLISHED, LOCKED
    status = Column(SQLEnum(HackathonStatus), default=HackathonStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    organizer_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)

    # Relationships
    organizer = relationship("User", foreign_keys=[organizer_id], back_populates="managed_hackathons")
    tracks = relationship("Track", back_populates="hackathon", cascade="all, delete-orphan")
    prizes = relationship("Prize", cascade="all, delete-orphan")
    teams = relationship("Team", back_populates="hackathon", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="hackathon", cascade="all, delete-orphan")
    judges = relationship("Judge", back_populates="hackathon", cascade="all, delete-orphan")
    rubrics = relationship("Rubric", back_populates="hackathon", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="hackathon", cascade="all, delete-orphan")
    registrations = relationship("Registration", back_populates="hackathon", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="hackathon", cascade="all, delete-orphan")
