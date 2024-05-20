from sqlalchemy.orm import Session

import models, schemas


def get_staff(db: Session, staff_id: int):
    return db.query(models.Staff).filter(models.Staff.id == staff_id).first()


def get_staff_by_email(db: Session, email: str):
    return db.query(models.Staff).filter(models.Staff.email == email).first()


def get_staffs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Staff).offset(skip).limit(limit).all()


def create_staff(db: Session, staff: schemas.StaffCreate):
    fake_hashed_password = staff.password + "notreallyhashed"
    db_staff = models.Staff(email=staff.email, name=staff.name, password=fake_hashed_password, role=staff.role.value)
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff


def get_channels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Channel).offset(skip).limit(limit).all()


def get_channel(db: Session, id: int):
    return db.query(models.Channel).filter(models.Channel.id == id).first()


def create_channel(db: Session, channel: schemas.ChannelCreate, staff_id: int):
    print(channel.json())
    db_channel = models.Channel(name=channel.name, description=channel.description, department=channel.department.value, created_by=staff_id)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel
