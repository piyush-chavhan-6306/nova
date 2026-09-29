from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_user_optional, verify_hackathon_owner, UserIdentity
from app.utils.enums import UserRole
from app.schemas.team import (
    TeamCreate, TeamResponse, TeamInvitationCreate,
    TeamInvitationResponse, TeamInvitationAction
)
from app.services.team_service import TeamService

router = APIRouter(tags=["Teams"])


@router.post("/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team_in: TeamCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new team for a hackathon and assign creator as Team Lead."""
    service = TeamService(db)
    return service.create_team(team_in, current_user_id=current_user.id)


@router.get("/teams/{team_id}", response_model=TeamResponse)
def get_team(team_id: str, db: Session = Depends(get_db)):
    """Retrieve detailed team information and member list."""
    service = TeamService(db)
    return service.get_team(team_id)


@router.get("/hackathons/{hackathon_id}/teams", response_model=List[TeamResponse])
def list_teams_for_hackathon(
    hackathon_id: str,
    current_user: Optional[UserIdentity] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """List all registered teams for a hackathon."""
    if current_user and current_user.role == UserRole.ORGANIZER:
        verify_hackathon_owner(hackathon_id, current_user, db)
    service = TeamService(db)
    return service.list_teams_for_hackathon(hackathon_id)


@router.post("/teams/{team_id}/invites", response_model=TeamInvitationResponse, status_code=status.HTTP_201_CREATED)
def invite_team_member(
    team_id: str,
    invite_in: TeamInvitationCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send an invitation email to join the team (Team Lead only)."""
    service = TeamService(db)
    return service.invite_member(team_id, invite_in, current_user_id=current_user.id)


@router.post("/teams/invites/{invitation_id}/respond", response_model=TeamInvitationResponse)
def respond_to_invitation(
    invitation_id: str,
    action: TeamInvitationAction,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept or decline a team invitation."""
    service = TeamService(db)
    return service.respond_to_invitation(invitation_id, action, current_user_id=current_user.id)


@router.delete("/teams/{team_id}/members/{user_id}")
def remove_team_member(
    team_id: str,
    user_id: str,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a member from a team or leave team (Lead or self)."""
    service = TeamService(db)
    return service.remove_member(team_id, user_id_to_remove=user_id, current_user_id=current_user.id)
