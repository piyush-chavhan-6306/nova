from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import (
    get_current_user, require_judge, require_judge_peer_isolation, UserIdentity
)
from app.schemas.judging import (
    JudgeAssignmentCreate, BatchJudgeAssignmentCreate, JudgeAssignmentResponse,
    ReviewCreate, ReviewResponse
)
from app.services.judging_service import JudgingService

router = APIRouter(tags=["Judging"])


@router.post("/judge-assignments", response_model=JudgeAssignmentResponse, status_code=status.HTTP_201_CREATED)
@router.post("/judging/assignments", response_model=JudgeAssignmentResponse, status_code=status.HTTP_201_CREATED)
def assign_judge(
    assign_in: JudgeAssignmentCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Assign a judge to evaluate a submission with peer isolation validation."""
    service = JudgingService(db)
    return service.assign_judge(assign_in)


@router.post("/judge-assignments/batch", response_model=List[JudgeAssignmentResponse], status_code=status.HTTP_201_CREATED)
def batch_assign_judges(
    batch_in: BatchJudgeAssignmentCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Track-aware, workload-balanced batch assignment for a hackathon event."""
    service = JudgingService(db)
    return service.batch_assign_judges(batch_in)


@router.get("/judges/me/assignments", response_model=List[JudgeAssignmentResponse])
@router.get("/judging/my-assignments", response_model=List[JudgeAssignmentResponse])
def get_my_assignments(
    hackathon_id: Optional[str] = Query(None),
    current_user: UserIdentity = Depends(require_judge),
    db: Session = Depends(get_db)
):
    """Retrieve all assigned submissions for the currently authenticated judge."""
    service = JudgingService(db)
    return service.list_my_assignments(current_user_id=current_user.id, hackathon_id=hackathon_id)


@router.get("/judges/{judge_id}/assignments", response_model=List[JudgeAssignmentResponse])
@router.get("/judging/scores", response_model=List[JudgeAssignmentResponse])
def get_judge_peer_assignments(
    judge_id: Optional[str] = None,
    judge: Optional[str] = Query(None),
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve assignments for a target judge with strict peer isolation check."""
    target_id = judge_id or judge or "jdg_01"
    require_judge_peer_isolation(target_id, current_user)
    service = JudgingService(db)
    return service.list_my_assignments(current_user_id=target_id, hackathon_id=None)


@router.get("/hackathons/{hackathon_id}/assignments", response_model=List[JudgeAssignmentResponse])
def get_hackathon_assignments(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all judge assignments for a hackathon event."""
    service = JudgingService(db)
    return service.list_hackathon_assignments(hackathon_id)


@router.delete("/judge-assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(
    assignment_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete or reassign a judge assignment."""
    service = JudgingService(db)
    service.delete_assignment(assignment_id)
    return None


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
