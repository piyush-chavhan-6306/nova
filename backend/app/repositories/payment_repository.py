import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.utils.enums import PaymentStatus


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, payment_id: str) -> Optional[Payment]:
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def create_payment(self, registration_id: str, amount: float, currency: str = "USD") -> Payment:
        pay_id = f"pay_{uuid.uuid4().hex[:8]}"
        pay = Payment(
            id=pay_id,
            registration_id=registration_id,
            amount=amount,
            currency=currency,
            status=PaymentStatus.PENDING
        )
        self.db.add(pay)
        self.db.commit()
        self.db.refresh(pay)
        return pay

    def update_payment_status(self, payment_id: str, status: PaymentStatus, transaction_id: Optional[str] = None) -> Optional[Payment]:
        pay = self.get_by_id(payment_id)
        if pay:
            pay.status = status
            if transaction_id:
                pay.transaction_id = transaction_id
            self.db.add(pay)
            self.db.commit()
            self.db.refresh(pay)
        return pay
