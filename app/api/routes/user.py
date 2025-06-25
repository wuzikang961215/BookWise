from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models import User
from app.schemas.user import UserOut

router = APIRouter()

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user