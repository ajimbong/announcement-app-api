from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import api.crud.announcement as crud
from api.crud.channel import get_channel
from api.crud.staff import get_staff
import api.schemas.announcement as ann_schema
from api.schemas.extras import AnnouncementExtra
from api.dependencies import get_db

router = APIRouter(
    prefix="/announcements",
    tags=["Announcements"],
    dependencies=[]
)


@router.get("/", response_model=list[ann_schema.Announcement], status_code=status.HTTP_200_OK)
def get_announcements(channel_id: int, db: Session = Depends(get_db)):
    announcements = crud.get_announcements(db, channel_id)
    return announcements


@router.get("/{ann_id}", response_model=AnnouncementExtra, status_code=status.HTTP_200_OK)
def get_announcement(ann_id: int, db: Session = Depends(get_db)):
    db_announcement = crud.get_announcement(db, ann_id)
    if db_announcement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found")

    return db_announcement


@router.post("/", response_model=ann_schema.Announcement, status_code=status.HTTP_200_OK)
def create_announcement(announcement: ann_schema.AnnouncementCreate, db: Session = Depends(get_db)):
    """
    - Verify if Channel ID exists
    - Verify if Staff ID exists
    """

    channel_id = announcement.channel_id
    channel = get_channel(db, channel_id)
    if channel is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request with channel id does not exist")

    staff_id = announcement.staff_id
    staff = get_staff(db, staff_id)
    if staff is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request with staff id does not exist")

    return crud.create_announcement(db, announcement)


@router.put("/{ann_id}", response_model=ann_schema.Announcement, status_code=status.HTTP_200_OK)
def update_announcement(ann_id: int, announcement: ann_schema.AnnouncementUpdate, db: Session = Depends(get_db)):
    """
    - Verify if Announcement exists
    - Verify if Channel ID exists
    - Verify if Staff ID exists
    """

    db_announcement = crud.get_announcement(db, ann_id)
    if db_announcement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement doesn't exist")

    channel_id = announcement.channel_id
    channel = get_channel(db, channel_id)
    if channel is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request with channel id does not exist")

    staff_id = announcement.staff_id
    staff = get_staff(db, staff_id)
    if staff is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request with staff id does not exist")

    return crud.update_announcement(db, announcement, ann_id)


@router.delete("/{ann_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_announcement(ann_id: int, db: Session = Depends(get_db)):
    """
    - Verify if announcement exists
    - Perform Delete action
    """

    db_announcement = crud.get_announcement(db, ann_id)
    if db_announcement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement doesn't exist")

    crud.delete_announcement(db, ann_id)
    return JSONResponse(content={"detail": "Announcement deleted"})
