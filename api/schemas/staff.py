from pydantic import BaseModel, EmailStr
from .enums import Role
from datetime import datetime
from typing import Optional, List
from .channel import Channel


class StaffBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[Role] = None
    created_by: Optional[int] = None


class StaffCreate(StaffBase):
    password: str


class Staff(StaffBase):
    id: int
    created_at: datetime
    updated_at: datetime
    channels: List['Channel']

    class Config:
        from_attributes = True
