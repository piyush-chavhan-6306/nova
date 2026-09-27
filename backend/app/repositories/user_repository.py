import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def count_users(self) -> int:
        return self.db.query(User).count()

    def create(self, user_in: UserCreate, hashed_password: str) -> User:
        user_id = f"usr_{uuid.uuid4().hex[:8]}"
        user = User(
            id=user_id,
            email=user_in.email,
            hashed_password=hashed_password,
            name=user_in.name,
            role=user_in.role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
