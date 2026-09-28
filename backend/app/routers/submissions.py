from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_user_optional, UserIdentity
from app.schemas.submission import SubmissionCreate, SubmissionUpdate, SubmissionResponse
from app.services.submission_service import SubmissionService

router = APIRouter(tags=["Submissions"])


@router.post("/submissions", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
def create_submission(
    sub_in: SubmissionCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a project submission draft or final submission for a team."""
    service = SubmissionService(db)
    return service.create_submission(sub_in, current_user_id=current_user.id)


@router.put("/submissions/{submission_id}", response_model=SubmissionResponse)
def update_submission(
    submission_id: str,
    sub_in: SubmissionUpdate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing project submission (Team member only)."""
    service = SubmissionService(db)
    return service.update_submission(submission_id, sub_in, current_user_id=current_user.id)


@router.get("/submissions/{submission_id}", response_model=SubmissionResponse)
def get_submission(
    submission_id: str,
    current_user: Optional[UserIdentity] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Retrieve details of a specific submission with optional blind review masking."""
    service = SubmissionService(db)
    return service.get_submission(submission_id, current_user=current_user)
