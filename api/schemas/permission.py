from pydantic import BaseModel

from .enums import AccessLevel
from datetime import datetime
from typing import Optional


class PermissionBase(BaseModel):
    channel_id: int
    staff_id: int
    access_level: Optional[AccessLevel] = AccessLevel.READ
    

class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class PermissionDelete(PermissionBase):
    pass


class Permission(PermissionBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attribute = True
    