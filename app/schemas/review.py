from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewOut(BaseModel):
    id: str
    booking_id: str
    user_id: str
    theme_id: str
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ReviewUser(BaseModel):
    id: str
    username: str

    class Config:
        from_attributes = True

class ReviewWithUserOut(BaseModel):
    id: str
    rating: int
    comment: Optional[str]
    created_at: datetime
    user: ReviewUser

    class Config:
        from_attributes = True
