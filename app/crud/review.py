from sqlalchemy.orm import Session
from app.models import Review

def create_review(db: Session, review: Review) -> Review:
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_reviews_for_theme(db: Session, theme_id: str):
    return (
        db.query(Review)
        .filter(Review.theme_id == theme_id)
        .order_by(Review.created_at.desc())
        .all()
    )
