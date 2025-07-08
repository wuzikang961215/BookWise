from pydantic import BaseModel, Field
from typing import Optional
from app.models import MerchantCategory

class MerchantOut(BaseModel):
    id: str
    name: str
    description: Optional[str]
    location: Optional[str]
    category: Optional[str]

    class Config:
        from_attributes = True

class MerchantCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    location: Optional[str] = None
    category: MerchantCategory