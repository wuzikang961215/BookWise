from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.core.security import get_current_user
from app.crud.slot import get_slot_availability as get_slot_availability_crud, get_slots_by_theme as get_slots_by_theme_crud
from app.schemas.slot import SlotOut, SlotCreate
from app.services.slots import create_slot_for_theme
from app.models import User

router = APIRouter()

@router.get("/themes/{theme_id}/slots", response_model=List[SlotOut])
def get_slots_by_theme(theme_id: str, db: Session = Depends(get_db)):
    return get_slots_by_theme_crud(db, theme_id)

@router.get("/slots/{slot_id}/availability")
def get_slot_availability(
    slot_id: str,
    db: Session = Depends(get_db)
):
    
    return get_slot_availability_crud(slot_id, db)

@router.post("/themes/{theme_id}/slots", response_model=SlotOut)
def create_slot(
    slot_in: SlotCreate,
    theme_id: str = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_slot_for_theme(
        db=db,
        current_user=current_user,
        theme_id=theme_id,
        slot_in=slot_in,
    )
