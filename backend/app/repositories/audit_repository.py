import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def log_action(
        self,
        action: str,
        user_id: Optional[str] = None,
        hackathon_id: Optional[str] = None,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
        details: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        log_id = f"aud_{uuid.uuid4().hex[:8]}"
        log = AuditLog(
            id=log_id,
            hackathon_id=hackathon_id,
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
            ip_address=ip_address
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def list_logs(self, hackathon_id: Optional[str] = None, limit: int = 100) -> List[AuditLog]:
        query = self.db.query(AuditLog)
        if hackathon_id:
            query = query.filter(AuditLog.hackathon_id == hackathon_id)
        return query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
