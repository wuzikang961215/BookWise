# app/api/routes/payments.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.payment import PaymentOut
from app.services.payments import get_payment_by_booking_id
from app.core.security import get_current_user

router = APIRouter()

@router.get("/bookings/{booking_id}/payment", response_model=PaymentOut)
def get_payment_route(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_payment_by_booking_id(db, booking_id, current_user.id)
