from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.crud.channel as crud
from api.schemas import channel as channel_schema
from api.dependencies import get_db

router = APIRouter(
    prefix="/channels",
    tags=["Channels"],
    dependencies=[]
)


@router.get("/", response_model=list[channel_schema.Channel])
def read_channel(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    channels = crud.get_channels(db, skip=skip, limit=limit)
    return channels
