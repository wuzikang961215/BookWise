from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.models import Theme, Slot, Merchant
from app.db import get_db
from dotenv import load_dotenv
from uuid import uuid4
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def backfill_missing_themes(session: Session):
    # 1. 获取所有已存在的 theme_id
    existing_theme_ids = {t.id for t in session.query(Theme.id).all()}
    
    # 2. 从 slots 中找出引用了但不存在的 theme_id
    used_theme_ids = {s.theme_id for s in session.query(Slot.theme_id).all()}
    missing_theme_ids = used_theme_ids - existing_theme_ids
    
    print(f"🔍 Found {len(missing_theme_ids)} missing themes to backfill.")

    # 3. 找一个 merchant 分配给缺失的 theme（或者你可以更复杂地分配）
    fallback_merchant = session.query(Merchant).first()
    if not fallback_merchant:
        print("❌ No merchant found. Cannot backfill themes.")
        return

    for theme_id in missing_theme_ids:
        theme = Theme(
            id=theme_id,
            merchant_id=fallback_merchant.id,
            title="Recovered Theme",
            description="Auto-recovered from orphaned slot reference.",
            price=0  # Default price
        )
        session.add(theme)

    session.commit()
    print(f"✅ Backfilled {len(missing_theme_ids)} themes.")

if __name__ == "__main__":
    with Session(engine) as session:
        backfill_missing_themes(session)
