from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from faker import Faker
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from app.models.models import Base, User, Merchant, Theme, Slot, MerchantCategory
from app.db import get_db
from dotenv import load_dotenv
import os, random
import requests

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
REGISTER_URL = "http://127.0.0.1:8000/api/auth/register"

engine = create_engine(DATABASE_URL)
fake = Faker()

def register_user(username, email, password="Test1234!"):
    try:
        res = requests.post(REGISTER_URL, json={
            "username": username,
            "email": email,
            "password": password
        })
        if res.status_code in (200, 201):
            print(f"✅ Registered {email}")
            return res.json().get("id")
        else:
            print(f"❌ Failed to register {email} ({res.status_code}): {res.text}")
            return None
    except Exception as e:
        print(f"❌ Exception during registration for {email}: {e}")
        return None

def seed_users_and_merchants(session, user_count=300, merchant_count=150, themes_per_merchant=6, slots_per_theme=12):
    fake.unique.clear()

    # Create regular users
    user_ids = []
    for _ in range(user_count):
        name = fake.unique.first_name()
        username = f"{name.lower()}_{uuid4().hex[:4]}"
        email = f"{username}@example.com"
        user_id = register_user(username, email)
        if user_id:
            user_ids.append(user_id)
    print(f"✅ Created {len(user_ids)} users")

    # Create merchants and update user role
    merchants = []
    merchant_user_ids = []
    for _ in range(merchant_count):
        name = fake.unique.company()
        username = f"{name.lower().replace(' ', '_')}_{uuid4().hex[:4]}"
        email = f"{username}@merchant.com"
        user_id = register_user(username, email)
        if user_id:
            merchant = Merchant(
                id=str(uuid4()),
                user_id=user_id,
                name=name,
                description=fake.catch_phrase(),
                location=fake.city(),
                category=random.choice(list(MerchantCategory))
            )
            session.add(merchant)
            merchants.append(merchant)
            merchant_user_ids.append(user_id)
    session.commit()
    print(f"✅ Created {len(merchants)} merchants")

    # ✅ Update role to 'merchant' for relevant users
    if merchant_user_ids:
        session.query(User).filter(User.id.in_(merchant_user_ids)).update(
            {User.role: 'merchant'}, synchronize_session=False
        )
        session.commit()
        print(f"✅ Updated {len(merchant_user_ids)} users to role='merchant'")

    # Create themes
    themes = []
    for merchant in merchants:
        for _ in range(themes_per_merchant):
            theme = Theme(
                id=str(uuid4()),
                merchant_id=merchant.id,
                title=fake.sentence(nb_words=3).rstrip('.'),
                description=fake.text(max_nb_chars=150)
            )
            session.add(theme)
            themes.append(theme)
    session.commit()
    print(f"✅ Created {len(themes)} themes")

    # Create slots
    slots = []
    now = datetime.now(timezone.utc)
    for theme in themes:
        for _ in range(slots_per_theme):
            start = now + timedelta(days=random.randint(7, 60), hours=random.randint(8, 20))
            slot = Slot(
                id=str(uuid4()),
                theme_id=theme.id,
                start_time=start,
                end_time=start + timedelta(hours=1),
                capacity=random.randint(6, 20)
            )
            session.add(slot)
            slots.append(slot)
    session.commit()
    print(f"✅ Created {len(slots)} slots")

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    with next(get_db()) as db:
        seed_users_and_merchants(db)
    print("✅ Done seeding users, merchants, themes, and slots.")
