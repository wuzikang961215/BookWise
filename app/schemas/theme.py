from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ThemeCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0)

class ThemeOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    price: Decimal
    merchant_id: str

    class Config:
        from_attributes = True
