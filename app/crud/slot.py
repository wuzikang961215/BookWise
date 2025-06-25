# app/crud/slot.py
from sqlalchemy.orm import Session
from app.models import Slot

def get_slots_by_theme(db: Session, theme_id: str):
    return db.query(Slot).filter(Slot.theme_id == theme_id).all()
