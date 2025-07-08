from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.review import ReviewCreate, ReviewOut, ReviewWithUserOut
from app.db import get_db
from app.core.security import get_current_user
from app.services.reviews import create_review_for_theme, list_reviews_for_theme
from app.models import User

router = APIRouter()

@router.post("/themes/{theme_id}/review", response_model=ReviewOut)
def create_review(
    theme_id: str,
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_review_for_theme(
        db=db,
        current_user=current_user,
        theme_id=theme_id,
        review_in=review_in
    )


@router.get("/themes/{theme_id}/reviews", response_model=list[ReviewWithUserOut])
def get_reviews(
    theme_id: str,
    db: Session = Depends(get_db),
):
    return list_reviews_for_theme(db, theme_id)
