from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import merchant as merchant_crud
from app.schemas.merchant import MerchantOut
from typing import List, Optional

router = APIRouter()

@router.get("/merchants", response_model=List[MerchantOut])
def list_merchants(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return merchant_crud.get_all_merchants(
        db=db,
        limit=limit,
        offset=offset,
        category=category
    )
