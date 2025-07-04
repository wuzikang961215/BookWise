from pydantic import BaseModel
from typing import Optional

class ThemeOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    price: float  # ✅ 新增字段

    class Config:
        from_attributes = True
