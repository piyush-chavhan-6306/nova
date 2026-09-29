from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import (
    get_current_user, require_judge, require_organizer, require_judge_peer_isolation, verify_hackathon_owner, UserIdentity
)
from app.utils.enums import UserRole
from app.schemas.judging import (
    JudgeAssignmentCreate, BatchJudgeAssignmentCreate, JudgeAssignmentResponse,
    ReviewCreate, ReviewResponse
)
from app.schemas.judge import (
    JudgeCreate, JudgeUpdate, JudgeResponse, JudgeTrackCreate, JudgeTrackResponse
)
from app.schemas.rubric import (
    RubricCreate, RubricUpdate, RubricResponse, RubricDetailResponse,
    RubricCriterionCreate, RubricCriterionUpdate, RubricCriterionResponse
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
    if current_user.role == UserRole.ORGANIZER:
        verify_hackathon_owner(hackathon_id, current_user, db)
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


# --- Judge Invitation & Management ---

@router.get("/hackathons/{hackathon_id}/judges", response_model=List[JudgeResponse])
def list_judges_for_hackathon(
    hackathon_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List judges registered for a hackathon."""
    if current_user.role == UserRole.ORGANIZER:
        verify_hackathon_owner(hackathon_id, current_user, db)
    service = JudgingService(db)
    return service.list_judges(hackathon_id)


@router.post("/hackathons/{hackathon_id}/judges", response_model=JudgeResponse, status_code=status.HTTP_201_CREATED)
def create_or_invite_judge(
    hackathon_id: str,
    judge_in: JudgeCreate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Invite or add a judge to a hackathon (Organizer/Admin only)."""
    verify_hackathon_owner(hackathon_id, current_user, db)
    service = JudgingService(db)
    return service.create_judge(hackathon_id, judge_in)


@router.put("/judges/{judge_id}", response_model=JudgeResponse)
def update_judge(
    judge_id: str,
    judge_in: JudgeUpdate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Update judge profile details."""
    service = JudgingService(db)
    judge = service.judging_repo.get_judge_by_id(judge_id)
    if judge:
        verify_hackathon_owner(judge.hackathon_id, current_user, db)
    return service.update_judge(judge_id, judge_in)


@router.delete("/judges/{judge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_judge(
    judge_id: str,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Revoke/remove judge access from a hackathon."""
    service = JudgingService(db)
    judge = service.judging_repo.get_judge_by_id(judge_id)
    if judge:
        verify_hackathon_owner(judge.hackathon_id, current_user, db)
    service.delete_judge(judge_id)


@router.post("/judges/{judge_id}/tracks", response_model=JudgeTrackResponse, status_code=status.HTTP_201_CREATED)
def assign_judge_track(
    judge_id: str,
    track_in: JudgeTrackCreate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Assign a track to a judge."""
    service = JudgingService(db)
    judge = service.judging_repo.get_judge_by_id(judge_id)
    if judge:
        verify_hackathon_owner(judge.hackathon_id, current_user, db)
    return service.assign_judge_track(judge_id, track_in)


@router.delete("/judges/{judge_id}/tracks/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_judge_track(
    judge_id: str,
    track_id: str,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Remove a track assignment from a judge."""
    service = JudgingService(db)
    judge = service.judging_repo.get_judge_by_id(judge_id)
    if judge:
        verify_hackathon_owner(judge.hackathon_id, current_user, db)
    service.remove_judge_track(judge_id, track_id)


# --- Rubric & Criteria Management ---

@router.get("/hackathons/{hackathon_id}/rubrics", response_model=List[RubricResponse])
@router.get("/hackathons/{hackathon_id}/rubric", response_model=List[RubricResponse])
def list_rubrics(
    hackathon_id: str,
    db: Session = Depends(get_db)
):
    """Get rubrics for a hackathon event."""
    service = JudgingService(db)
    return service.list_rubrics(hackathon_id)


@router.post("/hackathons/{hackathon_id}/rubrics", response_model=RubricResponse, status_code=status.HTTP_201_CREATED)
@router.post("/hackathons/{hackathon_id}/rubric", response_model=RubricResponse, status_code=status.HTTP_201_CREATED)
def create_rubric(
    hackathon_id: str,
    rubric_in: RubricCreate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Create a weighted rubric for a hackathon (Organizer/Admin only)."""
    verify_hackathon_owner(hackathon_id, current_user, db)
    service = JudgingService(db)
    return service.create_rubric(hackathon_id, rubric_in)


@router.get("/rubrics/{rubric_id}", response_model=RubricDetailResponse)
def get_rubric(
    rubric_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed rubric info including criteria."""
    service = JudgingService(db)
    return service.get_rubric(rubric_id)


@router.put("/rubrics/{rubric_id}", response_model=RubricResponse)
def update_rubric(
    rubric_id: str,
    rubric_in: RubricUpdate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Update a rubric's metadata."""
    service = JudgingService(db)
    rubric = service.judging_repo.get_rubric(rubric_id)
    if rubric:
        verify_hackathon_owner(rubric.hackathon_id, current_user, db)
    return service.update_rubric(rubric_id, rubric_in)


@router.delete("/rubrics/{rubric_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rubric(
    rubric_id: str,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Delete a rubric."""
    service = JudgingService(db)
    rubric = service.judging_repo.get_rubric(rubric_id)
    if rubric:
        verify_hackathon_owner(rubric.hackathon_id, current_user, db)
    service.delete_rubric(rubric_id)


@router.post("/rubrics/{rubric_id}/criteria", response_model=RubricCriterionResponse, status_code=status.HTTP_201_CREATED)
def create_rubric_criterion(
    rubric_id: str,
    crit_in: RubricCriterionCreate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Add a scoring criterion with weight to a rubric."""
    service = JudgingService(db)
    rubric = service.judging_repo.get_rubric(rubric_id)
    if rubric:
        verify_hackathon_owner(rubric.hackathon_id, current_user, db)
    return service.create_criterion(rubric_id, crit_in)


@router.put("/rubric-criteria/{criterion_id}", response_model=RubricCriterionResponse)
def update_rubric_criterion(
    criterion_id: str,
    crit_in: RubricCriterionUpdate,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Update a rubric criterion's name or weight."""
    service = JudgingService(db)
    crit = service.judging_repo.get_criterion(criterion_id)
    if crit and crit.rubric:
        verify_hackathon_owner(crit.rubric.hackathon_id, current_user, db)
    return service.update_criterion(criterion_id, crit_in)


@router.delete("/rubric-criteria/{criterion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rubric_criterion(
    criterion_id: str,
    current_user: UserIdentity = Depends(require_organizer),
    db: Session = Depends(get_db)
):
    """Delete a rubric criterion."""
    service = JudgingService(db)
    crit = service.judging_repo.get_criterion(criterion_id)
    if crit and crit.rubric:
        verify_hackathon_owner(crit.rubric.hackathon_id, current_user, db)
    service.delete_criterion(criterion_id)

