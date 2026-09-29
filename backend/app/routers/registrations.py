from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_user_optional, verify_hackathon_owner, UserIdentity
from app.utils.enums import UserRole
from app.schemas.registration import RegistrationCreate, RegistrationResponse
from app.services.registration_service import RegistrationService

router = APIRouter(tags=["Registrations"])


@router.post("/registrations", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_for_hackathon(
    reg_in: RegistrationCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register current user for a hackathon event."""
    service = RegistrationService(db)
    return service.register_user(reg_in, current_user_id=current_user.id)


@router.get("/hackathons/{hackathon_id}/registrations", response_model=List[RegistrationResponse])
def list_hackathon_registrations(
    hackathon_id: str,
    current_user: Optional[UserIdentity] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """List all registered participants for a hackathon."""
    if current_user and current_user.role == UserRole.ORGANIZER:
        verify_hackathon_owner(hackathon_id, current_user, db)
    service = RegistrationService(db)
    return service.list_registrations(hackathon_id)
