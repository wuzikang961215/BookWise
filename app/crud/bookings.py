from sqlalchemy.orm import Session, joinedload
from app.models import Booking, BookingStatus


def get_existing_active_booking(db: Session, user_id: str, slot_id: str):
    return db.query(Booking).filter(
        Booking.user_id == user_id,
        Booking.slot_id == slot_id,
        Booking.status != BookingStatus.cancelled
    ).first()


def get_confirmed_bookings_by_slot(db: Session, slot_id: str):
    return (
        db.query(Booking)
        .options(joinedload(Booking.user))
        .filter(
            Booking.slot_id == slot_id,
            Booking.status == BookingStatus.confirmed
        )
        .order_by(Booking.created_at)
        .all()
    )

def count_confirmed_bookings(db: Session, slot_id: str):
    return db.query(Booking).filter(
        Booking.slot_id == slot_id,
        Booking.status == BookingStatus.confirmed
    ).count()


def create_booking(db: Session, booking: Booking):
    db.add(booking)
