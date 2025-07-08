from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SlotCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    capacity: int = Field(..., ge=0)

class SlotOut(BaseModel):
    id: str
    theme_id: str
    start_time: datetime
    end_time: datetime
    capacity: int

    class Config:
        from_attributes = True
