from pydantic import BaseModel, EmailStr
from enum import Enum
from app.models import UserRole


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # assuming you collect password on registration
    role: UserRole = UserRole.user  # 👈 Default to "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: UserRole

    class Config:
        orm_mode = True  # or "model_config = {'from_attributes': True}" for Pydantic v2
