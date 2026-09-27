import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import RegistrationStatus


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(String, primary_key=True, index=True)
    hackathon_id = Column(String, ForeignKey("hackathons.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(SQLEnum(RegistrationStatus), default=RegistrationStatus.CONFIRMED, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    hackathon = relationship("Hackathon", back_populates="registrations")
    user = relationship("User", back_populates="registrations")
    payments = relationship("Payment", back_populates="registration", cascade="all, delete-orphan")
