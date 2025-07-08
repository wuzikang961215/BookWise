from sqlalchemy.orm import Session
from app.models import User
from app.crud.user import get_user_by_id

def fetch_user_by_id(user_id: str, db: Session) -> User:
    user = get_user_by_id(user_id, db)
    if not user:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
