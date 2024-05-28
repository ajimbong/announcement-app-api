from pydantic import BaseModel
from .enums import Department
from datetime import datetime


class ChannelBase(BaseModel):
    name: str
    description: str | None = None
    department: Department
    created_by: int


class ChannelCreate(ChannelBase):
    pass


class ChannelUpdate(ChannelBase):
    pass


class Channel(ChannelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
