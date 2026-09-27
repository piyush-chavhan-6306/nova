import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(String, primary_key=True, index=True)
    hackathon_id = Column(String, ForeignKey("hackathons.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    hackathon = relationship("Hackathon", back_populates="tracks")
    submissions = relationship("Submission", back_populates="track")
    judge_tracks = relationship("JudgeTrack", back_populates="track", cascade="all, delete-orphan")
