# app/api/routes/themes.py
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import theme as theme_crud
from app.schemas.theme import ThemeCreate, ThemeOut
from typing import List
from app.models import User
from app.services.themes import create_theme_for_merchant
from app.core.security import get_current_user

router = APIRouter()

@router.get("/merchants/{merchant_id}/themes", response_model=List[ThemeOut])
def get_themes_by_merchant(merchant_id: str, db: Session = Depends(get_db)):
    return theme_crud.get_themes_by_merchant(db, merchant_id)
    
@router.post("/merchants/{merchant_id}/themes", response_model=ThemeOut)
def create_theme(
    theme_in: ThemeCreate,  # ✅ comes first
    merchant_id: str = Path(..., description="Merchant ID to create theme under"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_theme_for_merchant(
        db=db,
        current_user=current_user,
        target_merchant_id=merchant_id,
        theme_in=theme_in,
    )
