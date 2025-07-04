# app/schemas/payment.py

from pydantic import BaseModel
from typing import Optional
from app.models import PaymentStatus, PaymentMethod

class PaymentOut(BaseModel):
    id: str
    amount: float
    method: PaymentMethod
    status: PaymentStatus
    payment_intent_id: Optional[str]

    class Config:
        from_attributes = True
