import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.registration import Registration
from app.utils.enums import RegistrationStatus


class RegistrationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, reg_id: str) -> Optional[Registration]:
        return self.db.query(Registration).filter(Registration.id == reg_id).first()

    def get_by_user_and_hackathon(self, user_id: str, hackathon_id: str) -> Optional[Registration]:
        return self.db.query(Registration).filter(
            Registration.user_id == user_id,
            Registration.hackathon_id == hackathon_id
        ).first()

    def create(self, hackathon_id: str, user_id: str, status: RegistrationStatus = RegistrationStatus.CONFIRMED) -> Registration:
        reg_id = f"reg_{uuid.uuid4().hex[:8]}"
        reg = Registration(
            id=reg_id,
            hackathon_id=hackathon_id,
            user_id=user_id,
            status=status
        )
        self.db.add(reg)
        self.db.commit()
        self.db.refresh(reg)
        return reg

    def update_status(self, reg_id: str, status: RegistrationStatus) -> Optional[Registration]:
        reg = self.get_by_id(reg_id)
        if reg:
            reg.status = status
            self.db.add(reg)
            self.db.commit()
            self.db.refresh(reg)
        return reg

    def list_by_hackathon(self, hackathon_id: str) -> List[Registration]:
        return self.db.query(Registration).filter(Registration.hackathon_id == hackathon_id).all()
