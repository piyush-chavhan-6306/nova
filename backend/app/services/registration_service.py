from typing import List
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, NotFoundException
from app.repositories.registration_repository import RegistrationRepository
from app.repositories.hackathon_repository import HackathonRepository
from app.repositories.audit_repository import AuditRepository
from app.schemas.registration import RegistrationCreate, RegistrationResponse
from app.utils.enums import RegistrationStatus, HackathonStatus


class RegistrationService:
    def __init__(self, db: Session):
        self.db = db
        self.reg_repo = RegistrationRepository(db)
        self.hack_repo = HackathonRepository(db)
        self.audit_repo = AuditRepository(db)

    def register_user(self, reg_in: RegistrationCreate, current_user_id: str) -> RegistrationResponse:
        hackathon = self.hack_repo.get_by_id(reg_in.hackathon_id)
        if not hackathon:
            raise NotFoundException("Hackathon", reg_in.hackathon_id)

        if hackathon.status in [HackathonStatus.CLOSED, HackathonStatus.ARCHIVED]:
            raise BadRequestException("Registrations are closed for this hackathon")

        existing = self.reg_repo.get_by_user_and_hackathon(current_user_id, reg_in.hackathon_id)
        if existing:
            return RegistrationResponse.model_validate(existing)

        status = RegistrationStatus.CONFIRMED
        reg = self.reg_repo.create(hackathon_id=reg_in.hackathon_id, user_id=current_user_id, status=status)

        # Log audit event
        self.audit_repo.log_action(
            action="USER_REGISTERED",
            user_id=current_user_id,
            hackathon_id=reg_in.hackathon_id,
            target_type="Registration",
            target_id=reg.id
        )

        return RegistrationResponse.model_validate(reg)

    def list_registrations(self, hackathon_id: str) -> List[RegistrationResponse]:
        regs = self.reg_repo.list_by_hackathon(hackathon_id)
        return [RegistrationResponse.model_validate(r) for r in regs]
