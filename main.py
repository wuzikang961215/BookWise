from fastapi import FastAPI
from app.api.routes import merchants
from app.api.routes import auth
from app.api.routes import user  
from app.api.routes import themes
from app.api.routes import slots
from app.api.routes import bookings  # ⬅️ your webhook is here

app = FastAPI()

@app.get("/")
def root():
    return {"message": "BookWise backend is live 🚀"}

# Consistent naming for tags (capitalization)
app.include_router(merchants.router, prefix="/api", tags=["merchants"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(themes.router, prefix="/api", tags=["themes"])
app.include_router(slots.router, prefix="/api", tags=["slots"])  # 🔽 changed to lowercase for consistency
app.include_router(bookings.router, prefix="/api", tags=["bookings"])  # ✅ added this line
