from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, UserIdentity
from app.schemas.payment import PaymentCheckoutCreate, PaymentWebhookPayload, PaymentResponse
from app.services.payment_service import PaymentService

router = APIRouter(tags=["Payments"])


@router.post("/payments/checkout", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment_checkout(
    checkout_in: PaymentCheckoutCreate,
    current_user: UserIdentity = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initiate payment checkout for a hackathon registration."""
    service = PaymentService(db)
    return service.create_checkout(checkout_in)


@router.post("/payments/webhook", response_model=PaymentResponse)
def handle_payment_webhook(
    payload: PaymentWebhookPayload,
    db: Session = Depends(get_db)
):
    """Handle external payment gateway webhook callbacks."""
    service = PaymentService(db)
    return service.process_webhook(payload)
