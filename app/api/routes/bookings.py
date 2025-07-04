from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.booking import BookingCreateRequest, BookingOut
from app.core.security import get_current_user
from app.services import bookings as booking_service

router = APIRouter()

@router.post("/slots/{slot_id}/book", response_model=BookingOut)
def book_slot(
    slot_id: str,
    booking_data: BookingCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return booking_service.create_booking_and_payment(
        db=db,
        user_id=current_user.id,
        slot_id=slot_id,
        booking_data=booking_data
    )
