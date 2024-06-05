from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import api.crud.channel as crud
import api.crud.staff as staff
from api.schemas import channel as channel_schema
from api.schemas.extras import ChannelExtra
from api.dependencies import get_db

router = APIRouter(
    prefix="/channels",
    tags=["Channels"],
    dependencies=[]
)


@router.get("/", response_model=list[channel_schema.Channel])
def get_channels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    channels = crud.get_channels(db, skip=skip, limit=limit)
    return channels


@router.get("/{channel_id}", response_model=ChannelExtra, status_code=status.HTTP_200_OK)
def get_single_channel(channel_id: int, db: Session = Depends(get_db)):
    db_channel = crud.get_channel(db, channel_id)

    if db_channel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")

    return db_channel


@router.post("/", response_model=channel_schema.Channel, status_code=status.HTTP_200_OK)
def create_channel(channel: channel_schema.ChannelCreate, db: Session = Depends(get_db)):
    """
    - Verify if staff ID exists
    """
    staff_id: int = channel.created_by
    db_staff = staff.get_staff(db, staff_id)
    if db_staff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    return crud.create_channel(db, channel, staff_id)


@router.put("/{channel_id}", response_model=channel_schema.Channel, status_code=status.HTTP_200_OK)
def update_channel(channel_id: int, channel: channel_schema.ChannelUpdate, db: Session = Depends(get_db)):
    """
    - Verify if channel exists
    - Verify if staff ID exists
    - Perform update operation
    """
    db_channel = crud.get_channel(db, channel_id)

    if db_channel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")

    staff_id: int = channel.created_by
    db_staff = staff.get_staff(db, staff_id)
    if db_staff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    return crud.update_channel(db, channel, channel_id)


@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel(channel_id: int, db: Session = Depends(get_db)):
    """
    - Verify if channel exists
    """
    db_channel = crud.get_channel(db, channel_id)
    if db_channel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")

    crud.delete_channel(db, channel_id)
    return JSONResponse(content={"detail": "Channel deleted"})
