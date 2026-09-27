from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestException, NotFoundException
from app.repositories.payment_repository import PaymentRepository
from app.repositories.registration_repository import RegistrationRepository
from app.repositories.audit_repository import AuditRepository
from app.schemas.payment import PaymentCheckoutCreate, PaymentWebhookPayload, PaymentResponse
from app.utils.enums import PaymentStatus, RegistrationStatus


class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.pay_repo = PaymentRepository(db)
        self.reg_repo = RegistrationRepository(db)
        self.audit_repo = AuditRepository(db)

    def create_checkout(self, checkout_in: PaymentCheckoutCreate) -> PaymentResponse:
        reg = self.reg_repo.get_by_id(checkout_in.registration_id)
        if not reg:
            raise NotFoundException("Registration", checkout_in.registration_id)

        payment = self.pay_repo.create_payment(
            registration_id=checkout_in.registration_id,
            amount=checkout_in.amount,
            currency=checkout_in.currency
        )

        return PaymentResponse.model_validate(payment)

    def process_webhook(self, payload: PaymentWebhookPayload) -> PaymentResponse:
        payment = self.pay_repo.get_by_id(payload.payment_id)
        if not payment:
            raise NotFoundException("Payment", payload.payment_id)

        new_status = PaymentStatus.SUCCESS if payload.success else PaymentStatus.FAILED
        updated_pay = self.pay_repo.update_payment_status(
            payment_id=payment.id,
            status=new_status,
            transaction_id=payload.transaction_id
        )

        if payload.success:
            self.reg_repo.update_status(payment.registration_id, RegistrationStatus.CONFIRMED)
            self.audit_repo.log_action(
                action="PAYMENT_SUCCESS",
                user_id=payment.registration.user_id if payment.registration else None,
                hackathon_id=payment.registration.hackathon_id if payment.registration else None,
                target_type="Payment",
                target_id=payment.id,
                details=f"Transaction: {payload.transaction_id}"
            )

        return PaymentResponse.model_validate(updated_pay)
