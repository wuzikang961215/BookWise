from sqlalchemy.orm import Session
from app.models.models import Merchant
from typing import Optional

def get_all_merchants(
    db: Session,
    limit: int = 20,
    offset: int = 0,
    category: Optional[str] = None
):
    query = db.query(Merchant)
    if category:
        query = query.filter(Merchant.category == category)
    return query.offset(offset).limit(limit).all()
