from datetime import datetime
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
    action: Optional[str] = Query(None),
    actor_id: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None, alias="from"),
    to_date: Optional[datetime] = Query(None, alias="to"),
    limit: int = Query(100, ge=1, le=500),
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Query system audit logs with filters (Organizer / Admin only)."""
    service = AuditService(db)
    return service.get_audit_logs(
        current_user=current_user,
        hackathon_id=hackathon_id,
        action=action,
        actor_id=actor_id,
        entity_type=entity_type,
        from_date=from_date,
        to_date=to_date,
        limit=limit
    )


@router.get("/hackathons/{hackathon_id}/audit-logs", response_model=List[AuditLogResponse])
def get_hackathon_audit_logs(
    hackathon_id: str,
    action: Optional[str] = Query(None),
    actor_id: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None, alias="from"),
    to_date: Optional[datetime] = Query(None, alias="to"),
    limit: int = Query(100, ge=1, le=500),
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get audit logs for a specific hackathon with optional filtering."""
    service = AuditService(db)
    return service.get_audit_logs(
        current_user=current_user,
        hackathon_id=hackathon_id,
        action=action,
        actor_id=actor_id,
        entity_type=entity_type,
        from_date=from_date,
        to_date=to_date,
        limit=limit
    )
