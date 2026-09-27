import datetime
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False, default="")
    hashed_password = Column(String, nullable=True)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.PARTICIPANT)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    team_memberships = relationship("TeamMember", back_populates="user", cascade="all, delete-orphan")
    judge_profile = relationship("Judge", back_populates="user", uselist=False, cascade="all, delete-orphan")
    registrations = relationship("Registration", back_populates="user", cascade="all, delete-orphan")
