from app.db import get_db
from app.models.models import User
from app.core.security import hash_password, create_refresh_token

print("🔍 Starting script...")

db = next(get_db())

print("📥 Querying users without credentials...")
users = db.query(User).filter(User.hashed_password == None).all()

print(f"🔍 Found {len(users)} users to update")

updated = 0
for user in users:
    user.hashed_password = hash_password("defaultpassword123")
    user.refresh_token = create_refresh_token({"sub": user.id})
    updated += 1
    print(f"✅ Updated user {user.email}")

db.commit()
print(f"🎉 Finished updating {updated} users.")
