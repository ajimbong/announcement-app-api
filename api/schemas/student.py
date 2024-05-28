from datetime import datetime

from pydantic import BaseModel, EmailStr


# TODO: Add Regex Validation for matricule
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    matricule: str


class StudentCreate(StudentBase):
    password: str


class StudentUpdate(StudentBase):
    password: str


class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
