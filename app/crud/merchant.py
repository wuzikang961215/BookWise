from sqlalchemy.orm import Session
from app.models.models import Merchant
from typing import Optional
from app.schemas.merchant import MerchantCreate
import uuid

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


def create_merchant(db: Session, merchant_in: MerchantCreate, user_id: str) -> Merchant:
    merchant = Merchant(
        id=str(uuid.uuid4()),
        user_id=user_id,
        name=merchant_in.name,
        description=merchant_in.description,
        location=merchant_in.location,
        category=merchant_in.category,
    )
    db.add(merchant)
    return merchant  # DO NOT commit here