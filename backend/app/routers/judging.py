from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, UserIdentity
from app.schemas.judging import (
    JudgeAssignmentCreate, JudgeAssignmentResponse,
    ReviewCreate, ReviewResponse
)
from app.services.judging_service import JudgingService

router = APIRouter(tags=["Judging"])


@router.post("/judging/assignments", response_model=JudgeAssignmentResponse, status_code=status.HTTP_201_CREATED)
def assign_judge(
    assign_in: JudgeAssignmentCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Assign a judge to evaluate a submission with peer isolation validation."""
    service = JudgingService(db)
    return service.assign_judge(assign_in)


@router.get("/judging/my-assignments", response_model=List[JudgeAssignmentResponse])
def get_my_assignments(
    hackathon_id: str = Query(...),
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve all assigned submissions for the currently authenticated judge."""
    service = JudgingService(db)
    return service.list_my_assignments(current_user_id=current_user.id, hackathon_id=hackathon_id)


@router.post("/judging/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def submit_review(
    rev_in: ReviewCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit evaluation review and scores for a submission."""
    service = JudgingService(db)
    return service.submit_review(rev_in, current_user_id=current_user.id)


@router.get("/judging/submissions/{submission_id}/reviews", response_model=List[ReviewResponse])
def get_reviews_for_submission(
    submission_id: str,
    db: Session = Depends(get_db)
):
    """List all submitted reviews for a project submission."""
    service = JudgingService(db)
    return service.get_reviews_for_submission(submission_id)
