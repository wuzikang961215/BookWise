from app.models.models import Base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

print("Creating all missing tables...")
Base.metadata.create_all(bind=engine)
print("✅ Done.")
