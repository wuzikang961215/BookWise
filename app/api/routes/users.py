from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud.user import get_all_users
from app.core.security import get_current_user
from app.models import User, UserRole
from app.services.bookings import get_detailed_bookings_for_user
from app.services.users import fetch_user_by_id
from app.schemas.user import UserOut
from app.schemas.booking import BookingDetailOut

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def read_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
    return get_all_users(db)

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/me/bookings", response_model=List[BookingDetailOut])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_detailed_bookings_for_user(current_user.id, db)

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id_route(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
    return fetch_user_by_id(user_id, db)