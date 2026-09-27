from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.audit_repository import AuditRepository
from app.schemas.audit_log import AuditLogResponse


class AuditService:
    def __init__(self, db: Session):
        self.db = db
        self.audit_repo = AuditRepository(db)

    def get_audit_logs(self, hackathon_id: Optional[str] = None, limit: int = 100) -> List[AuditLogResponse]:
        logs = self.audit_repo.list_logs(hackathon_id=hackathon_id, limit=limit)
        return [AuditLogResponse.model_validate(l) for l in logs]
