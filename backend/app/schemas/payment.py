from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.utils.enums import PaymentStatus


class PaymentCheckoutCreate(BaseModel):
    registration_id: str
    amount: float = Field(..., gt=0)
    currency: str = "USD"


class PaymentWebhookPayload(BaseModel):
    payment_id: str
    transaction_id: str
    success: bool


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    registration_id: str
    amount: float
    currency: str
    status: PaymentStatus
    transaction_id: Optional[str] = None
    created_at: datetime
