# test_connection.py
from sqlalchemy import create_engine

engine = create_engine("postgresql://bookwise_user:bookwise_pass@db:5432/bookwise")

try:
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("✅ Connected to database:", result.scalar())
except Exception as e:
    print("❌ Connection failed:", e)
