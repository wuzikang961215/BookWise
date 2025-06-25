# app/schemas/slot.py
from pydantic import BaseModel
from datetime import datetime

class SlotOut(BaseModel):
    id: str
    start_time: datetime
    end_time: datetime
    capacity: int
    booked_count: int

    class Config:
        orm_mode = True
