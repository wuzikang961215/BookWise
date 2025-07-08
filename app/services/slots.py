from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models import Slot, Theme, User, UserRole
from app.schemas.slot import SlotCreate
from app.crud.slot import create_slot as create_slot_crud
import uuid

def create_slot_for_theme(
    db: Session,
    current_user: User,
    theme_id: str,
    slot_in: SlotCreate
) -> Slot:
    # Step 1: Load theme
    theme = db.query(Theme).filter(Theme.id == theme_id).first()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    # Step 2: Permission check
    if current_user.role == UserRole.admin:
        pass
    elif current_user.role == UserRole.merchant:
        if not current_user.merchant_profile or current_user.merchant_profile.id != theme.merchant_id:
            raise HTTPException(status_code=403, detail="You cannot create a slot for this theme.")
    else:
        raise HTTPException(status_code=403, detail="Only merchants or admins can create slots.")

    # Step 3: Optional: validate time
    if slot_in.end_time <= slot_in.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time.")

    new_slot = Slot(
        id=str(uuid.uuid4()),
        theme_id=theme_id,
        start_time=slot_in.start_time,
        end_time=slot_in.end_time,
        capacity=slot_in.capacity
    )

    try:
        return create_slot_crud(db, new_slot)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A slot with this start and end time already exists for this theme."
        )