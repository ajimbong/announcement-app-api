from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import api.crud.staff as crud
from api.crud.channel import create_channel
import api.schemas.staff as staff_schema
import api.schemas.channel as chanel_schema
from api.dependencies import get_db

router = APIRouter(
    prefix="/staffs",
    tags=["Staffs"],
    dependencies=[]
)


@router.get("/", response_model=list[staff_schema.Staff])
def read_staffs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    staffs = crud.get_staffs(db, skip=skip, limit=limit)
    return staffs


@router.get("/{staff_id}", response_model=staff_schema.Staff)
def read_staff(staff_id: int, db: Session = Depends(get_db)):
    db_staff = crud.get_staff(db, staff_id=staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff Account not found")
    return db_staff


@router.post("/", response_model=staff_schema.Staff, status_code=status.HTTP_201_CREATED)
def create_staff(staff: staff_schema.StaffCreate, db: Session = Depends(get_db)):
    db_staff = crud.get_staff_by_email(db, email=staff.email)
    if db_staff:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Email already registered")
    return crud.create_staff(db=db, staff=staff)


@router.post("/{user_id}/channels/", response_model=chanel_schema.Channel)
def create_channel_with_staff_id(
        user_id: int, channel: chanel_schema.ChannelCreate, db: Session = Depends(get_db)
):
    return create_channel(db=db, channel=channel, staff_id=user_id)
