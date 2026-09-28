from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, UserIdentity
from app.schemas.judge_conflict import ConflictDeclareCreate, ConflictResponse
from app.services.judge_conflict_service import JudgeConflictService

router = APIRouter(tags=["Judge Conflicts & Recusal"])


@router.post("/judges/me/conflicts", response_model=ConflictResponse, status_code=status.HTTP_201_CREATED)
def declare_conflict(
    create_in: ConflictDeclareCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Declare a conflict of interest or recusal request for a judge."""
    service = JudgeConflictService(db)
    return service.declare_conflict(create_in, current_user)


@router.get("/judges/me/conflicts", response_model=List[ConflictResponse])
def get_my_conflicts(
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List conflicts declared by current logged-in judge."""
    service = JudgeConflictService(db)
    return service.list_my_conflicts(current_user)


@router.get("/hackathons/{hackathon_id}/conflicts", response_model=List[ConflictResponse])
def get_hackathon_conflicts(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all declared conflicts for a hackathon (Organizer / Admin only)."""
    service = JudgeConflictService(db)
    return service.list_hackathon_conflicts(hackathon_id, current_user)


@router.post("/judge-conflicts/{conflict_id}/resolve", response_model=ConflictResponse)
def resolve_conflict(
    conflict_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resolve/Approve a declared conflict of interest."""
    service = JudgeConflictService(db)
    return service.resolve_conflict(conflict_id, action="resolve", current_user=current_user)


@router.post("/judge-conflicts/{conflict_id}/reject", response_model=ConflictResponse)
def reject_conflict(
    conflict_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject a declared conflict of interest."""
    service = JudgeConflictService(db)
    return service.resolve_conflict(conflict_id, action="reject", current_user=current_user)
