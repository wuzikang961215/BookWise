# app/crud/slot.py
from sqlalchemy.orm import Session
from app.models import Slot, Booking, BookingStatus
from fastapi import HTTPException, status

def get_slots_by_theme(db: Session, theme_id: str):
    return db.query(Slot).filter(Slot.theme_id == theme_id).all()

def get_slot_availability(slot_id: str, db: Session):
    slot = db.query(Slot).filter(Slot.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")

    confirmed = db.query(Booking).filter(
        Booking.slot_id == slot_id,
        Booking.status == BookingStatus.confirmed
    ).count()

    return {
        "capacity": slot.capacity,
        "confirmed_count": confirmed,
        "remaining_spots": max(0, slot.capacity - confirmed)
    }

def create_slot(db: Session, slot: Slot) -> Slot:
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot

