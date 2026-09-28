import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class CalibrationSet(Base):
    __tablename__ = "calibration_sets"

    id = Column(String, primary_key=True, index=True)
    hackathon_id = Column(String, ForeignKey("hackathons.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="ACTIVE", nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    hackathon = relationship("Hackathon")
    projects = relationship("CalibrationProject", back_populates="calibration_set", cascade="all, delete-orphan")


class CalibrationProject(Base):
    __tablename__ = "calibration_projects"

    id = Column(String, primary_key=True, index=True)
    calibration_set_id = Column(String, ForeignKey("calibration_sets.id", ondelete="CASCADE"), nullable=False, index=True)
    submission_id = Column(String, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, index=True)
    expected_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    calibration_set = relationship("CalibrationSet", back_populates="projects")
    submission = relationship("Submission")


class CalibrationResult(Base):
    __tablename__ = "calibration_results"

    id = Column(String, primary_key=True, index=True)
    calibration_set_id = Column(String, ForeignKey("calibration_sets.id", ondelete="CASCADE"), nullable=False, index=True)
    judge_id = Column(String, ForeignKey("judges.id", ondelete="CASCADE"), nullable=False, index=True)
    submission_id = Column(String, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    deviation = Column(Float, nullable=False)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    calibration_set = relationship("CalibrationSet")
    judge = relationship("Judge")
    submission = relationship("Submission")
