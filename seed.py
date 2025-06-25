from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from faker import Faker
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from app.db import get_db
from app.models.models import (
    Base, User, Merchant, Theme, Slot,
    Booking, Payment, Review, PaymentStatus
)
from dotenv import load_dotenv
import os, random

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
fake = Faker()

def generate_unique_users(count, start_index=162050):
    users = []
    for i in range(count):
        index = i + start_index
        users.append(User(
            id=str(uuid4()),
            username=f"user_{index}",
            email=f"user_{index}@example.com",
            is_merchant=False,
            created_at=datetime.utcnow()
        ))
    return users



# ✅ 批量插入预订 + 支付 + 评论
def bulk_insert_bookings_and_payments(session, users, slots, batch_size=5000, total=100000):
    bookings, payments, reviews = [], [], []
    statuses = ["pending", "confirmed", "cancelled"]
    methods = ["credit_card", "paypal", "mock"]
    payment_statuses = list(PaymentStatus)

    for i in range(total):
        user = random.choice(users)
        slot = random.choice(slots)
        booking_id = str(uuid4())
        created = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 180))

        bookings.append({
            "id": booking_id,
            "user_id": user.id,
            "slot_id": slot.id,
            "status": random.choice(statuses),
            "created_at": created
        })
        payments.append({
            "id": str(uuid4()),
            "booking_id": booking_id,
            "user_id": user.id,
            "amount": Decimal(random.randint(10, 100)),
            "method": random.choice(methods),
            "status": random.choice(payment_statuses),
            "created_at": created
        })
        if random.random() < 0.5:
            reviews.append({
                "id": str(uuid4()),
                "user_id": user.id,
                "theme_id": slot.theme_id,
                "rating": random.randint(3, 5),
                "comment": fake.sentence(),
                "created_at": created
            })

        if i % batch_size == 0 and i > 0:
            session.bulk_insert_mappings(Booking, bookings)
            session.bulk_insert_mappings(Payment, payments)
            session.bulk_insert_mappings(Review, reviews)
            session.commit()
            bookings.clear()
            payments.clear()
            reviews.clear()

    if bookings:
        session.bulk_insert_mappings(Booking, bookings)
        session.bulk_insert_mappings(Payment, payments)
        session.bulk_insert_mappings(Review, reviews)
        session.commit()


def seed_all(session, user_count=10000, merchant_count=200, themes_per_merchant=10, slots_per_theme=10):
    # ✅ 用户
    users = generate_unique_users(user_count)
    session.bulk_save_objects(users)
    session.commit()

    # ✅ 商户 + 商户用户
    merchants = []
    for i in range(merchant_count):
        merchant_user = User(
            id=str(uuid4()),
            username=f"{fake.user_name()}_merchant_{i}",
            email=f"{fake.email().split('@')[0]}_merchant_{i}@example.com",
            is_merchant=True,
            created_at=datetime.now(timezone.utc)
        )
        merchant = Merchant(
            id=str(uuid4()),
            user_id=merchant_user.id,
            name=fake.company(),
            description=fake.catch_phrase(),
            location=fake.city()
        )
        users.append(merchant_user)
        merchants.append(merchant)
        session.add_all([merchant_user, merchant])
    session.commit()

    # ✅ 主题
    themes = []
    for merchant in merchants:
        for _ in range(themes_per_merchant):
            theme = Theme(
                id=str(uuid4()),
                merchant_id=merchant.id,
                title=fake.bs().title(),
                description=fake.text()
            )
            themes.append(theme)
            session.add(theme)
    session.commit()

    # ✅ 时段
    slots = []
    for theme in themes:
        for _ in range(slots_per_theme):
            slot = Slot(
                id=str(uuid4()),
                theme_id=theme.id,
                start_time=datetime.now(timezone.utc) + timedelta(days=random.randint(1, 60)),
                capacity=random.randint(5, 15)
            )
            slots.append(slot)
            session.add(slot)
    session.commit()

    # ✅ 插入预订、支付、评论
    bulk_insert_bookings_and_payments(session, users, slots, total=100000)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    seed_all(db)
    print("✅ Done seeding all data.")
