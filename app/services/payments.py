from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Payment, Booking, PaymentStatus, BookingStatus
from app.db import SessionLocal
from app.tasks.stripe import create_stripe_payment_intent


def kickoff_payment_intent(payment_id: str, booking_id: str, user_id: str, amount: float):
    create_stripe_payment_intent.delay(
        payment_id=payment_id,
        booking_id=booking_id,
        user_id=user_id,
        amount=amount
    )


def get_payment_by_booking_id(db: Session, booking_id: str, user_id: str):
    payment = db.query(Payment).filter(Payment.booking_id == booking_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return payment


def handle_stripe_webhook(payload: dict):
    event_type = payload.get("type")
    data_object = payload.get("data", {}).get("object", {})

    if event_type != "payment_intent.succeeded":
        raise ValueError("Unhandled event type")

    metadata = data_object.get("metadata", {})
    booking_id = metadata.get("booking_id")
    user_id = metadata.get("user_id")
    payment_intent_id = data_object.get("id")

    if not all([booking_id, user_id, payment_intent_id]):
        raise ValueError("Missing metadata")

    process_stripe_webhook(payment_intent_id, booking_id, user_id)


def process_stripe_webhook(payment_intent_id: str, booking_id: str, user_id: str):
    with SessionLocal() as db:
        try:
            payment = db.query(Payment).filter(
                Payment.booking_id == booking_id,
                Payment.user_id == user_id
            ).first()

            if not payment:
                raise ValueError("Payment not found")

            if payment.status == PaymentStatus.success:
                return  # Already processed

            booking = db.query(Booking).filter(
                Booking.id == booking_id,
                Booking.user_id == user_id
            ).first()

            if not booking:
                raise ValueError("Booking not found")

            payment.payment_intent_id = payment_intent_id
            payment.status = PaymentStatus.success
            booking.status = BookingStatus.confirmed

            db.commit()
        except Exception:
            db.rollback()
            raise