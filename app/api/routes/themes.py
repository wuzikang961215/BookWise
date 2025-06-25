# app/api/routes/themes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import theme as theme_crud
from app.schemas.theme import ThemeOut
from typing import List

router = APIRouter()

@router.get("/merchants/{merchant_id}/themes", response_model=List[ThemeOut])
def get_themes_by_merchant(merchant_id: str, db: Session = Depends(get_db)):
    return theme_crud.get_themes_by_merchant(db, merchant_id)
