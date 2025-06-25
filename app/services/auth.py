# app/services/auth.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt, JWTError
from app.crud import user as crud_user
from app.core import security
from app.models import User, UserRole
from app.core.security import (
    issue_token_pair,
    verify_password,
    SECRET_KEY,
    ALGORITHM
)


def register_user(db: Session, user_in):
    if user_in.role != UserRole.user:
        raise HTTPException(status_code=403, detail="Cannot register as admin or merchant")
    return crud_user.create_user(db, user_in)


def login_user(db: Session, email: str, password: str) -> dict:
    user = authenticate_user(db, email, password)
    tokens = issue_token_pair(user.id)
    user.refresh_token = tokens["refresh_token"]
    db.commit()
    return tokens


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = crud_user.get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


def refresh_token_flow(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise credentials_exception
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).get(user_id)
    if not user or user.refresh_token != token:
        raise HTTPException(status_code=401, detail="Refresh token mismatch")

    new_tokens = issue_token_pair(user_id)
    user.refresh_token = new_tokens["refresh_token"]
    db.commit()
    return new_tokens


def get_user_from_access_token(token: str, db: Session) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise credentials_exception
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
