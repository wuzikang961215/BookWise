from sqlalchemy.orm import Session
from app.models import Theme

def get_themes_by_merchant(db: Session, merchant_id: str):
    return db.query(Theme).filter(Theme.merchant_id == merchant_id).all()
