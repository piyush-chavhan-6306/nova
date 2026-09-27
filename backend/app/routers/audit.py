from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, UserIdentity
from app.schemas.audit_log import AuditLogResponse
from app.services.audit_service import AuditService

router = APIRouter(tags=["Audit Logs"])


@router.get("/audit-logs", response_model=List[AuditLogResponse])
def get_audit_logs(
    hackathon_id: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Query system audit logs for administrative oversight."""
    service = AuditService(db)
    return service.get_audit_logs(hackathon_id=hackathon_id, limit=limit)
