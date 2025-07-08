from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import PaymentMethod, BookingStatus, PaymentStatus

class BookingCreateRequest(BaseModel):
    payment_method: PaymentMethod

class BookingOut(BaseModel):
    id: str
    slot_id: str
    status: BookingStatus
    payment_method: PaymentMethod
    created_at: datetime
    payment_id: Optional[str]
    payment_status: Optional[str]  # 或 Enum
    # Optional: include slot details for convenience
    # slot: Optional[SlotOut]

    class Config:
        from_attributes = True

class ThemeBrief(BaseModel):
    id: str
    title: str

    class Config:
        from_attributes = True

class SlotBrief(BaseModel):
    id: str
    start_time: datetime
    end_time: datetime
    theme: ThemeBrief

    class Config:
        from_attributes = True

class BookingDetailOut(BaseModel):
    id: str
    status: BookingStatus
    payment_method: PaymentMethod
    created_at: datetime
    payment_id: Optional[str]
    payment_status: Optional[PaymentStatus]
    slot: SlotBrief

    class Config:
        from_attributes = True