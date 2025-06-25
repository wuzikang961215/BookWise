# app/api/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.schemas.user import UserOut, UserCreate, UserLogin
from app.schemas.auth import TokenResponse
from app.db import get_db
from app.services import auth as auth_service
from app.core.security import get_bearer_token


router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user_in)


@router.post("/login", response_model=TokenResponse)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db, user_in.email, user_in.password)


@router.post("/refresh", response_model=TokenResponse)
def refresh(token: str = Depends(get_bearer_token), db: Session = Depends(get_db)):
    return auth_service.refresh_token_flow(token, db)