from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class JudgeTrack(Base):
    __tablename__ = "judge_tracks"

    id = Column(String, primary_key=True, index=True)
    judge_id = Column(String, ForeignKey("judges.id", ondelete="CASCADE"), nullable=False, index=True)
    track_id = Column(String, ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relationships
    judge = relationship("Judge", back_populates="assigned_tracks")
    track = relationship("Track", back_populates="judge_tracks")
