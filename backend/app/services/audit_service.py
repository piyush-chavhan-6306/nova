from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.audit_repository import AuditRepository
from app.schemas.audit_log import AuditLogResponse
from app.core.dependencies import UserIdentity, verify_hackathon_owner
from app.core.exceptions import ForbiddenException
from app.utils.enums import UserRole


class AuditService:
    def __init__(self, db: Session):
        self.db = db
        self.audit_repo = AuditRepository(db)

    def get_audit_logs(
        self,
        current_user: Optional[UserIdentity] = None,
        hackathon_id: Optional[str] = None,
        action: Optional[str] = None,
        actor_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[AuditLogResponse]:
        if current_user and current_user.role == UserRole.ORGANIZER:
            if hackathon_id:
                verify_hackathon_owner(hackathon_id, current_user, self.db)

        logs = self.audit_repo.list_logs(
            hackathon_id=hackathon_id,
            action=action,
            actor_id=actor_id,
            entity_type=entity_type,
            from_date=from_date,
            to_date=to_date,
            limit=limit
        )
        return [AuditLogResponse.model_validate(l) for l in logs]
