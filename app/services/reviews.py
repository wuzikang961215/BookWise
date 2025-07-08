from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User, UserRole, Booking, BookingStatus, PaymentStatus, Review, Slot
from app.schemas.review import ReviewCreate
from app.crud.review import create_review as create_review_crud, get_reviews_for_theme
import uuid

def create_review_for_theme(
    db: Session,
    current_user: User,
    theme_id: str,
    review_in: ReviewCreate
) -> Review:
    # Find a booking that belongs to the user, is completed, paid, and matches the theme
    booking = db.query(Booking).join(Slot).filter(
        Booking.user_id == current_user.id,
        Booking.status == BookingStatus.confirmed,
        Booking.payment.has(status=PaymentStatus.success),
        Slot.theme_id == theme_id
    ).order_by(Booking.created_at.desc()).first()

    if not booking:
        raise HTTPException(status_code=400, detail="You have no eligible completed & paid booking for this theme.")

    review = Review(
        id=str(uuid.uuid4()),
        booking_id=booking.id,
        user_id=current_user.id,
        theme_id=theme_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )

    try:
        return create_review_crud(db, review)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="You have already submitted a review for this booking.")


def list_reviews_for_theme(db: Session, theme_id: str):
    return get_reviews_for_theme(db, theme_id)
