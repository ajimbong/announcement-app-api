from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.crud.staff import get_staff_by_email
from api.crud.student import get_student_by_email
from api.db.models import Student as StudentModel, Staff as StaffModel
from api.schemas.token import Token, StudentJWT, StaffJWT
from api.utils.dependencies import get_db
from api.utils.hashing import verify_password
from api.utils.token import create_access_token

router = APIRouter(
    prefix="/login",
    tags=["Auth"]
)


@router.post("/student", response_model=Token, status_code=status.HTTP_200_OK)
def student_login(request: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
    - Verify if student exists in our database
    - Verify if student's password matched
    - Generate token and send
    """

    db_student: StudentModel = get_student_by_email(db, request.username)
    if db_student is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    if verify_password(request.password, db_student.password) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    student_data: StudentJWT = StudentJWT(
        id=db_student.id,
        email=db_student.email,
    )

    access_token = create_access_token(data=student_data.dict())

    return Token(access_token=access_token, token_type="Bearer")


@router.post("/staff", response_model=Token, status_code=status.HTTP_200_OK)
def student_login( request: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
    - Verify if staff exists in our database
    - Verify if Staff's password is hashed
    - Generate token and send
    """

    db_staff: StaffModel = get_staff_by_email(db, request.username)
    if db_staff is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    if verify_password(request.password, db_staff.password) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    staff_data: StaffJWT = StaffJWT(
        id=db_staff.id,
        email=db_staff.email,
        role=db_staff.role,
    )

    access_token = create_access_token(data=staff_data.dict())

    return Token(access_token=access_token, token_type="Bearer")
