import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Judge(Base):
    __tablename__ = "judges"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    hackathon_id = Column(String, ForeignKey("hackathons.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="judge_profile")
    hackathon = relationship("Hackathon", back_populates="judges")
    assigned_tracks = relationship("JudgeTrack", back_populates="judge", cascade="all, delete-orphan")
    assignments = relationship("JudgeAssignment", back_populates="judge", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="judge", cascade="all, delete-orphan")
