from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_organizer, UserIdentity
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserIdentity = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve profile of the currently authenticated user."""
    service = AuthService(db)
    return service.get_user_by_id(current_user.id)


@router.get("", response_model=List[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """List all registered users (Organizer/Admin only)."""
    repo = UserRepository(db)
    users = repo.list_users(skip=skip, limit=limit)
    return [UserResponse.model_validate(u) for u in users]
