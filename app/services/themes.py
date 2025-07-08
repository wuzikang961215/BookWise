from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models import Theme, User, UserRole
from app.schemas.theme import ThemeCreate
from app.crud.theme import create_theme as create_theme_crud

import uuid


def create_theme_for_merchant(
    db: Session,
    current_user: User,
    target_merchant_id: str,
    theme_in: ThemeCreate
) -> Theme:
    # ✅ Permission check
    if current_user.role == UserRole.admin:
        pass  # Admins can override
    elif current_user.role == UserRole.merchant:
        if not current_user.merchant_profile or current_user.merchant_profile.id != target_merchant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot create a theme for another merchant."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only merchants or admins can create themes."
        )

    new_theme = Theme(
        id=str(uuid.uuid4()),
        merchant_id=target_merchant_id,
        title=theme_in.title,
        description=theme_in.description,
        price=theme_in.price,
    )

    try:
        return create_theme_crud(db, new_theme)
    except IntegrityError as e:
        db.rollback()
        if 'uq_merchant_title' in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A theme with this title already exists for this merchant."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database constraint error."
        )
