import uuid
import secrets
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.team import Team
from app.models.team_member import TeamMember
from app.models.team_invitation import TeamInvitation
from app.models.user import User
from app.schemas.team import TeamCreate, TeamUpdate, TeamInvitationCreate
from app.utils.enums import TeamRole, InvitationStatus


class TeamRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, team_id: str) -> Optional[Team]:
        return (
            self.db.query(Team)
            .options(joinedload(Team.members).joinedload(TeamMember.user))
            .filter(Team.id == team_id)
            .first()
        )

    def list_teams_for_hackathon(self, hackathon_id: str) -> List[Team]:
        return (
            self.db.query(Team)
            .options(joinedload(Team.members).joinedload(TeamMember.user))
            .filter(Team.hackathon_id == hackathon_id)
            .all()
        )

    def get_user_membership_in_hackathon(self, user_id: str, hackathon_id: str) -> Optional[TeamMember]:
        return (
            self.db.query(TeamMember)
            .join(Team, Team.id == TeamMember.team_id)
            .filter(TeamMember.user_id == user_id, Team.hackathon_id == hackathon_id)
            .first()
        )

    def create_team(self, team_in: TeamCreate, creator_id: str) -> Team:
        team_id = f"team_{uuid.uuid4().hex[:8]}"
        join_code = secrets.token_hex(4).upper()
        team = Team(
            id=team_id,
            hackathon_id=team_in.hackathon_id,
            name=team_in.name,
            join_code=join_code,
        )
        self.db.add(team)

        # Add creator as LEAD
        member_id = f"tm_{uuid.uuid4().hex[:8]}"
        creator_member = TeamMember(
            id=member_id,
            team_id=team_id,
            user_id=creator_id,
            role=TeamRole.LEAD,
        )
        self.db.add(creator_member)

        self.db.commit()
        self.db.refresh(team)
        return self.get_by_id(team_id)

    def update_team(self, team: Team, team_in: TeamUpdate) -> Team:
        if team_in.name:
            team.name = team_in.name
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team

    def add_member(self, team_id: str, user_id: str, role: TeamRole = TeamRole.MEMBER) -> TeamMember:
        member_id = f"tm_{uuid.uuid4().hex[:8]}"
        member = TeamMember(
            id=member_id,
            team_id=team_id,
            user_id=user_id,
            role=role,
        )
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def remove_member(self, member: TeamMember):
        self.db.delete(member)
        self.db.commit()

    def get_member(self, team_id: str, user_id: str) -> Optional[TeamMember]:
        return (
            self.db.query(TeamMember)
            .filter(TeamMember.team_id == team_id, TeamMember.user_id == user_id)
            .first()
        )

    # Invitations
    def create_invitation(self, team_id: str, email: str) -> TeamInvitation:
        inv_id = f"inv_{uuid.uuid4().hex[:8]}"
        token = secrets.token_urlsafe(16)
        invitation = TeamInvitation(
            id=inv_id,
            team_id=team_id,
            email=email,
            token=token,
            status=InvitationStatus.PENDING,
        )
        self.db.add(invitation)
        self.db.commit()
        self.db.refresh(invitation)
        return invitation

    def get_invitation_by_id(self, invitation_id: str) -> Optional[TeamInvitation]:
        return self.db.query(TeamInvitation).filter(TeamInvitation.id == invitation_id).first()

    def get_invitation_by_token(self, token: str) -> Optional[TeamInvitation]:
        return self.db.query(TeamInvitation).filter(TeamInvitation.token == token).first()

    def update_invitation_status(self, invitation: TeamInvitation, status: InvitationStatus) -> TeamInvitation:
        invitation.status = status
        self.db.add(invitation)
        self.db.commit()
        self.db.refresh(invitation)
        return invitation
