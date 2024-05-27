from sqlalchemy.orm import Session

from api.schemas.staff import StaffCreate
from api.db import models


def get_staff(db: Session, staff_id: int):
    return db.query(models.Staff).filter(models.Staff.id == staff_id).first()


def get_staff_by_email(db: Session, email: str):
    return db.query(models.Staff).filter(models.Staff.email == email).first()


def get_staffs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Staff).offset(skip).limit(limit).all()


def create_staff(db: Session, staff: StaffCreate):
    fake_hashed_password = staff.password + "notreallyhashed"
    db_staff = models.Staff(email=staff.email, name=staff.name, password=fake_hashed_password, created_by=staff.created_by, role=staff.role.value)
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff