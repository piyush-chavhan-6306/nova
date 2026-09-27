from sqlalchemy import Column, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(String, primary_key=True, index=True)
    review_id = Column(String, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False, index=True)
    criterion_id = Column(String, ForeignKey("rubric_criteria.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)

    # Relationships
    review = relationship("Review", back_populates="scores")
    criterion = relationship("RubricCriterion", back_populates="scores")
