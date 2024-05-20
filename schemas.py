from pydantic import BaseModel, EmailStr
from enums import Role, Department
from datetime import datetime
from typing import Optional, List


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


class ChannelBase(BaseModel):
    name: str
    description: str | None = None
    department: Department
    created_by: int


class ChannelCreate(ChannelBase):
    pass


class Channel(ChannelBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # staff_created: Staff

    class Config:
        from_attributes = True
