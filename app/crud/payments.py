from sqlalchemy.orm import Session
from app.models import Payment


def create_payment(db: Session, payment: Payment):
    db.add(payment)
