from sqlalchemy.orm import Session

from api.schemas.staff import StaffCreate
from api.db import models
from api.utils.hashing import get_password_hash


def get_staff(db: Session, staff_id: int):
    return db.query(models.Staff).filter(models.Staff.id == staff_id).first()


def get_staff_by_email(db: Session, email: str):
    return db.query(models.Staff).filter(models.Staff.email == email).first()


def get_staffs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Staff).offset(skip).limit(limit).all()


# FIXME: We don't want staff members to update
# their roles by themselves. Only Staff accounts
# with Administrative rights should be able to
# do so
def create_staff(db: Session, staff: StaffCreate):
    hashed_password = get_password_hash(staff.password)
    db_staff = models.Staff(email=staff.email, name=staff.name, password=hashed_password, created_by=staff.created_by, role=staff.role.value)
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff
