from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from api.db.database import SessionLocal
from api.schemas.token import StudentJWT
from api.utils.token import decode_token


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Authentication Dependencies
student_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/student")

staff_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/staff")


async def get_current_student(token: Annotated[str, Depends(student_oauth2_scheme)]) -> StudentJWT:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    current_student: StudentJWT

    try:
        payload = decode_token(token)
        student_id: str = payload.get("id")
        email: str = payload.get("email")

        if student_id is None or email is None:
            raise credentials_exception
        current_student = StudentJWT(id=student_id, email=email)

    except InvalidTokenError:
        raise credentials_exception

    return current_student
