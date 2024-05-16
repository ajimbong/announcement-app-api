from pydantic import BaseModel
from enums import Role, Department
from datetime import datetime
from typing import Optional

class StaffBase(BaseModel):
    email: str
    role: Optional[Role]
    created_by: Optional[int]


class StaffCreate(StaffBase):
    password: str


class Staff(StaffBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


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
    staff_created: Staff

    class Config:
        orm_mode = True