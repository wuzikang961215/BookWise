# app/schemas/payment.py

from pydantic import BaseModel
from typing import Optional
from app.models import PaymentStatus, PaymentMethod
from datetime import datetime


class PaymentOut(BaseModel):
    id: str
    booking_id: str
    user_id: str
    amount: float
    method: PaymentMethod
    status: PaymentStatus
    payment_intent_id: str | None
    created_at: datetime

    class Config:
        from_attributes = True