import string

from pydantic import BaseModel, EmailStr, field_validator, Field
from pydantic_core.core_schema import FieldValidationInfo

from .enums import Role
from datetime import datetime
from typing import Optional, List


class StaffBase(BaseModel):
    name: str
    email: EmailStr
    role: Role = Role.OTHER
    created_by: Optional[int] = None


class StaffCreate(StaffBase):
    password: str = Field(examples=["Password123#"])
    confirm_password: str = Field(examples=["Password123#"])

    # Verify if password is strong
    @field_validator('password')
    def password_valid(cls, v):
        if len(v) < 8:
            raise ValueError("Password must have at least 8 characters")

        if not any(c.isupper() for c in v) or \
                not any(c.islower() for c in v) or \
                not any(c.isdigit() for c in v) or \
                not any(c in string.punctuation for c in v):
            raise ValueError("Password must include a digit, lowercase, uppercase and special character")
        return v

    # Verifies if passwords match
    @field_validator('confirm_password')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('passwords do not match')
        return v


class StaffUpdate(StaffBase):
    pass


class Staff(StaffBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
