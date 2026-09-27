from typing import List
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, ForbiddenException, NotFoundException
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.team_repository import TeamRepository
from app.repositories.user_repository import UserRepository
from app.schemas.team import (
    TeamCreate, TeamUpdate, TeamResponse, TeamMemberResponse,
    TeamInvitationCreate, TeamInvitationResponse, TeamInvitationAction
)
from app.utils.enums import TeamRole, InvitationStatus


class TeamService:
    def __init__(self, db: Session):
        self.db = db
        self.team_repo = TeamRepository(db)
        self.hack_repo = HackathonRepository(db)
        self.user_repo = UserRepository(db)

    def _build_team_response(self, team) -> TeamResponse:
        members_resp = []
        for m in team.members:
            user_name = m.user.name if m.user else None
            user_email = m.user.email if m.user else None
            members_resp.append(
                TeamMemberResponse(
                    id=m.id,
                    team_id=m.team_id,
                    user_id=m.user_id,
                    role=m.role,
                    user_name=user_name,
                    user_email=user_email,
                    joined_at=m.joined_at,
                )
            )
        resp = TeamResponse.model_validate(team)
        resp.members = members_resp
        return resp

    def create_team(self, team_in: TeamCreate, current_user_id: str) -> TeamResponse:
        hackathon = self.hack_repo.get_by_id(team_in.hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{team_in.hackathon_id}' not found")

        # Check existing membership in hackathon
        existing = self.team_repo.get_user_membership_in_hackathon(current_user_id, team_in.hackathon_id)
        if existing:
            raise BadRequestException("You are already part of a team for this hackathon")

        team = self.team_repo.create_team(team_in, creator_id=current_user_id)
        return self._build_team_response(team)

    def get_team(self, team_id: str) -> TeamResponse:
        team = self.team_repo.get_by_id(team_id)
        if not team:
            raise NotFoundException(f"Team '{team_id}' not found")
        return self._build_team_response(team)

    def list_teams_for_hackathon(self, hackathon_id: str) -> List[TeamResponse]:
        hackathon = self.hack_repo.get_by_id(hackathon_id)
        if not hackathon:
            raise NotFoundException(f"Hackathon '{hackathon_id}' not found")
        teams = self.team_repo.list_teams_for_hackathon(hackathon_id)
        return [self._build_team_response(t) for t in teams]

    def invite_member(self, team_id: str, invite_in: TeamInvitationCreate, current_user_id: str) -> TeamInvitationResponse:
        team = self.team_repo.get_by_id(team_id)
        if not team:
            raise NotFoundException(f"Team '{team_id}' not found")

        # Verify current user is team LEAD
        member = self.team_repo.get_member(team_id, current_user_id)
        if not member or member.role != TeamRole.LEAD:
            raise ForbiddenException("Only the Team Lead can issue team invitations")

        # Check max team size
        hackathon = self.hack_repo.get_by_id(team.hackathon_id)
        if hackathon and len(team.members) >= hackathon.max_team_size:
            raise BadRequestException(f"Team has reached maximum allowed size ({hackathon.max_team_size})")

        # Create invitation
        invitation = self.team_repo.create_invitation(team_id, invite_in.email)
        return TeamInvitationResponse.model_validate(invitation)

    def respond_to_invitation(self, invitation_id: str, action: TeamInvitationAction, current_user_id: str) -> TeamInvitationResponse:
        invitation = self.team_repo.get_invitation_by_id(invitation_id)
        if not invitation:
            raise NotFoundException(f"Invitation '{invitation_id}' not found")

        if invitation.status != InvitationStatus.PENDING:
            raise BadRequestException(f"Invitation is already {invitation.status.value}")

        user = self.user_repo.get_by_id(current_user_id)
        if not user or user.email.lower() != invitation.email.lower():
            raise ForbiddenException("This invitation was not issued for your email address")

        if action.accept:
            team = self.team_repo.get_by_id(invitation.team_id)
            if team:
                # Add user to team
                self.team_repo.add_member(team.id, user.id, role=TeamRole.MEMBER)
            updated_inv = self.team_repo.update_invitation_status(invitation, InvitationStatus.ACCEPTED)
        else:
            updated_inv = self.team_repo.update_invitation_status(invitation, InvitationStatus.DECLINED)

        return TeamInvitationResponse.model_validate(updated_inv)

    def remove_member(self, team_id: str, user_id_to_remove: str, current_user_id: str):
        team = self.team_repo.get_by_id(team_id)
        if not team:
            raise NotFoundException(f"Team '{team_id}' not found")

        requester = self.team_repo.get_member(team_id, current_user_id)
        target = self.team_repo.get_member(team_id, user_id_to_remove)

        if not target:
            raise NotFoundException(f"User '{user_id_to_remove}' is not a member of team '{team_id}'")

        # Allow if requester is removing self, or requester is Team Lead
        if current_user_id != user_id_to_remove and (not requester or requester.role != TeamRole.LEAD):
            raise ForbiddenException("Only Team Leads can remove other members")

        self.team_repo.remove_member(target)
        return {"detail": f"User '{user_id_to_remove}' successfully removed from team"}
