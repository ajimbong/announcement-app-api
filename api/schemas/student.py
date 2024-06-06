import re
import string
from datetime import datetime

from pydantic import BaseModel, EmailStr, ValidationError, field_validator, Field
from pydantic_core.core_schema import FieldValidationInfo


# TODO: Add Regex Validation for matricule
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    matricule: str = Field(examples=["ET20200721"])

    @field_validator('matricule')
    def matricule_valid(cls, v):
        pattern = r'^[a-zA-Z]{2,3}\d{8}$'
        if re.match(pattern, v) is False:
            raise ValueError("Matricule must be of the form ET20200721")
        return v


class StudentCreate(StudentBase):
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


class StudentUpdate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
