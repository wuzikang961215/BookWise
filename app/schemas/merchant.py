from pydantic import BaseModel
from typing import Optional

class MerchantOut(BaseModel):
    id: str
    name: str
    description: Optional[str]
    location: Optional[str]
    category: Optional[str]

    class Config:
        from_attributes = True
