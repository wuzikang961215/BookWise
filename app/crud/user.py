# app/crud/user.py

from sqlalchemy.orm import Session
from app.models.models import User, UserRole
from app.schemas.user import UserCreate
from app.core.security import hash_password
import uuid
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def create_user(db: Session, user_in: UserCreate):
    user = User(
        id=str(uuid.uuid4()),
        username=user_in.username,
        email=user_in.email,
        role=user_in.role,
        hashed_password=hash_password(user_in.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email or username already registered")
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(user_id: str, db: Session) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def update_user_role(db: Session, user: User, new_role: UserRole):
    user.role = new_role
    db.add(user)
