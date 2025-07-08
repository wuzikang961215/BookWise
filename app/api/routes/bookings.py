from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Slot
from app.schemas.booking import BookingCreateRequest, BookingOut, BookingDetailOut
from app.crud.bookings import count_confirmed_bookings
from app.core.security import get_current_user
from app.services import bookings as booking_service
from app.models import User

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

@router.get("/slots/{slot_id}/bookings", response_model=list[BookingDetailOut])
def get_confirmed_bookings(
    slot_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return booking_service.fetch_confirmed_bookings_for_slot(db, current_user, slot_id)


@router.get("/slots/{slot_id}/booking-count")
def get_booking_count(slot_id: str, db: Session = Depends(get_db)):
    slot = db.query(Slot).filter(Slot.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    
    count = count_confirmed_bookings(db, slot_id)
    return {
        "slot_id": slot_id,
        "confirmed_count": count,
        "capacity": slot.capacity
    }