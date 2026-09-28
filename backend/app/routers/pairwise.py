from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, UserIdentity
from app.schemas.pairwise import (
    PairwiseEvaluationCreate, PairwiseEvaluationUpdate,
    PairwiseEvaluationResponse, PairwiseProgressResponse
)
from app.services.pairwise_service import PairwiseService

router = APIRouter(tags=["Pairwise Judging"])


@router.post("/pairwise-evaluations", response_model=PairwiseEvaluationResponse, status_code=status.HTTP_201_CREATED)
def create_pairwise_evaluation(
    create_in: PairwiseEvaluationCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or assign a pairwise project evaluation task for a judge."""
    service = PairwiseService(db)
    return service.create_evaluation(create_in, current_user)


@router.get("/judges/me/pairwise-evaluations", response_model=List[PairwiseEvaluationResponse])
def get_my_pairwise_evaluations(
    hackathon_id: str = Query(...),
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List pairwise evaluations assigned to the currently authenticated judge."""
    service = PairwiseService(db)
    return service.list_my_pairwise_evaluations(hackathon_id, current_user)


@router.get("/pairwise-evaluations/{eval_id}", response_model=PairwiseEvaluationResponse)
def get_pairwise_evaluation(
    eval_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of a specific pairwise evaluation."""
    service = PairwiseService(db)
    return service.get_evaluation(eval_id, current_user)


@router.put("/pairwise-evaluations/{eval_id}", response_model=PairwiseEvaluationResponse)
def update_pairwise_evaluation(
    eval_id: str,
    update_in: PairwiseEvaluationUpdate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update winner selection or reason for a pairwise evaluation."""
    service = PairwiseService(db)
    return service.update_evaluation(eval_id, update_in, current_user)


@router.post("/pairwise-evaluations/{eval_id}/submit", response_model=PairwiseEvaluationResponse)
def submit_pairwise_evaluation(
    eval_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit and lock judge's decision for a pairwise evaluation."""
    service = PairwiseService(db)
    return service.submit_evaluation(eval_id, current_user)


@router.post("/pairwise-evaluations/{eval_id}/lock", response_model=PairwiseEvaluationResponse)
def lock_pairwise_evaluation(
    eval_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lock a pairwise evaluation (Organizer/Admin only)."""
    service = PairwiseService(db)
    return service.lock_evaluation(eval_id, current_user)


@router.get("/hackathons/{hackathon_id}/pairwise-evaluations", response_model=List[PairwiseEvaluationResponse])
def get_hackathon_pairwise_evaluations(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all pairwise evaluations for a hackathon event (Organizer/Admin only)."""
    service = PairwiseService(db)
    return service.list_hackathon_pairwise(hackathon_id, current_user)


@router.get("/hackathons/{hackathon_id}/pairwise-progress", response_model=PairwiseProgressResponse)
def get_pairwise_progress(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve completion statistics for pairwise evaluations."""
    service = PairwiseService(db)
    return service.get_progress(hackathon_id, current_user)
