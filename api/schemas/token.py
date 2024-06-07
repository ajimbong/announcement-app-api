from pydantic import BaseModel, EmailStr

from api.schemas.enums import Role


class Token(BaseModel):
    access_token: str
    token_type: str


class StudentJWT(BaseModel):
    id: int
    email: EmailStr


class StaffJWT(BaseModel):
    id: int
    email: EmailStr
    role: str
