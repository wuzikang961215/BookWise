from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models import Booking, Payment, Slot, BookingStatus, PaymentStatus
from app.schemas.booking import BookingCreateRequest, BookingOut  # ✅ 注意添加 BookingOut
from app.crud import bookings as bookings_crud
from app.crud import payments as payments_crud
from app.services.payments import kickoff_payment_intent
import uuid


def create_booking_and_payment(db: Session, user_id: str, slot_id: str, booking_data: BookingCreateRequest) -> BookingOut:
    booking_id = str(uuid.uuid4())
    payment_id = str(uuid.uuid4())

    print(f"🟡 Creating booking... booking_id={booking_id}, payment_id={payment_id}, slot_id={slot_id}, user_id={user_id}")

    try:
        slot = db.query(Slot).filter(Slot.id == slot_id).with_for_update().first()
        print(f"🔎 Slot fetched: {slot}")
        if not slot:
            raise HTTPException(status_code=404, detail="Slot not found")

        existing = bookings_crud.get_existing_active_booking(db, user_id, slot_id)
        print(f"🔍 Existing active booking: {existing}")
        if existing:
            raise HTTPException(status_code=400, detail="You have already booked this slot")

        confirmed_count = bookings_crud.count_confirmed_bookings(db, slot_id)
        print(f"👥 Confirmed bookings: {confirmed_count} / {slot.capacity}")
        if confirmed_count >= slot.capacity:
            raise HTTPException(status_code=400, detail="This slot is fully booked")

        price = slot.theme.price if slot.theme else None
        print(f"💰 Price from theme: {price}")
        if price is None:
            raise HTTPException(status_code=500, detail="Theme price not set")

        booking = Booking(
            id=booking_id,
            user_id=user_id,
            slot_id=slot_id,
            status=BookingStatus.pending
        )
        bookings_crud.create_booking(db, booking)
        print(f"✅ Booking inserted: {booking.id}")

        payment = Payment(
            id=payment_id,
            booking_id=booking.id,
            user_id=user_id,
            amount=price,
            method=booking_data.payment_method,
            status=PaymentStatus.pending
        )
        payments_crud.create_payment(db, payment)
        print(f"✅ Payment inserted: {payment.id}")

        db.commit()
        print(f"🟢 DB committed")

    except IntegrityError:
        db.rollback()
        print(f"❌ IntegrityError — transaction rolled back")
        raise HTTPException(status_code=400, detail="Booking failed due to conflict")

    try:
        kickoff_payment_intent(
            payment_id=payment_id,
            booking_id=booking_id,
            user_id=user_id,
            amount=float(price)
        )
        print(f"📨 Stripe payment task dispatched")
    except Exception as e:
        print(f"⚠️ Failed to dispatch Stripe payment task: {e}")

    return BookingOut(
        id=booking.id,
        slot_id=slot_id,
        status=booking.status.value,
        created_at=booking.created_at, 
        payment_id=payment.id,
        payment_method=payment.method,
        payment_status=payment.status
    )
