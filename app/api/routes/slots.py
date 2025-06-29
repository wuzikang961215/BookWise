from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.crud import slot as slot_crud
from app.schemas.slot import SlotOut

router = APIRouter()

@router.get("/themes/{theme_id}/slots", response_model=List[SlotOut])
def get_slots_by_theme(theme_id: str, db: Session = Depends(get_db)):
    return slot_crud.get_slots_by_theme(db, theme_id)
