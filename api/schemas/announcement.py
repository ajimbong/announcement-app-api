from pydantic import BaseModel

from datetime import datetime


class AnnouncementBase(BaseModel):
    message: str
    channel_id: int
    staff_id: int


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementUpdate(AnnouncementBase):
    pass


class Announcement(AnnouncementBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes: True
