from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.core.security import get_current_user
from app.crud import merchant as merchant_crud
from app.models import User, UserRole
from app.schemas.merchant import MerchantOut, MerchantCreate
from app.services.merchants import create_merchant_and_update_role
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

@router.post("/merchants", response_model=MerchantOut, status_code=status.HTTP_201_CREATED)
def create_merchant(
    merchant_in: MerchantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.user:
        raise HTTPException(status_code=400, detail="Only normal users can become merchants")

    if current_user.merchant_profile:
        raise HTTPException(status_code=400, detail="User already has a merchant profile")

    return create_merchant_and_update_role(db, merchant_in, current_user)