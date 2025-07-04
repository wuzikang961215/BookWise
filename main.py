from fastapi import FastAPI
from app.api.routes import merchants
from app.api.routes import auth
from app.api.routes import user  
from app.api.routes import themes
from app.api.routes import slots
from app.api.routes import bookings 
from app.api.routes import payments  
from app.api.routes import webhooks

app = FastAPI()

@app.get("/")
def root():
    return {"message": "BookWise backend is live 🚀"}

# Consistent naming for tags (capitalization)
app.include_router(merchants.router, prefix="/api", tags=["merchants"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(themes.router, prefix="/api", tags=["themes"])
app.include_router(slots.router, prefix="/api", tags=["slots"])  
app.include_router(bookings.router, prefix="/api", tags=["bookings"])  
app.include_router(payments.router, prefix="/api", tags=["payments"])  
app.include_router(webhooks.router, prefix="/api", tags=["webhooks"])