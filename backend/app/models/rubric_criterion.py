import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class RubricCriterion(Base):
    __tablename__ = "rubric_criteria"

    id = Column(String, primary_key=True, index=True)
    rubric_id = Column(String, ForeignKey("rubrics.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False)
    weight = Column(Float, default=1.0, nullable=False)
    max_score = Column(Float, default=5.0, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    rubric = relationship("Rubric", back_populates="criteria")
    scores = relationship("Score", back_populates="criterion", cascade="all, delete-orphan")
