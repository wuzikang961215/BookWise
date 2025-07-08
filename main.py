from fastapi import FastAPI
from app.api.routes import merchants
from app.api.routes import auth
from app.api.routes import users 
from app.api.routes import themes
from app.api.routes import slots
from app.api.routes import bookings 
from app.api.routes import payments  
from app.api.routes import webhooks
from app.api.routes import reviews

app = FastAPI()

@app.get("/")
def root():
    return {"message": "BookWise backend is live 🚀"}

# Consistent naming for tags (capitalization)
app.include_router(merchants.router, prefix="/api", tags=["merchants"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(themes.router, prefix="/api", tags=["themes"])
app.include_router(slots.router, prefix="/api", tags=["slots"])  
app.include_router(bookings.router, prefix="/api", tags=["bookings"])  
app.include_router(payments.router, prefix="/api", tags=["payments"])  
app.include_router(webhooks.router, prefix="/api", tags=["webhooks"])
app.include_router(reviews.router, prefix="/api", tags=["webhooks"])