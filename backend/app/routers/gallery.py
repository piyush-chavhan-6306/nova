from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.submission import GalleryProjectResponse
from app.services.submission_service import SubmissionService

router = APIRouter(tags=["Gallery"])


@router.get("/gallery", response_model=List[GalleryProjectResponse])
@router.get("/projects", response_model=List[GalleryProjectResponse])
def get_public_gallery(
    hackathon_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Public Project Gallery Endpoint (NOVA Platform T1 Requirement).
    No authentication required. Returns published hackathon project submissions.
    """
    service = SubmissionService(db)
    return service.list_gallery_projects(hackathon_id=hackathon_id, skip=skip, limit=limit)
