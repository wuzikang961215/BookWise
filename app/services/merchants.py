from sqlalchemy.orm import Session
from app.models import User, UserRole
from app.schemas.merchant import MerchantCreate
from app.crud.merchant import create_merchant
from app.crud.user import update_user_role

def create_merchant_and_update_role(
    db: Session, merchant_in: MerchantCreate, user: User
):
    merchant = create_merchant(db, merchant_in, user.id)
    update_user_role(db, user, UserRole.merchant)
    db.commit()
    db.refresh(merchant)
    return merchant
