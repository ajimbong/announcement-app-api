from sqlalchemy.orm import Session

from api.db import models
from api.schemas.channel import ChannelCreate


def get_channels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Channel).offset(skip).limit(limit).all()


def get_channel(db: Session, id: int):
    return db.query(models.Channel).filter(models.Channel.id == id).first()


def create_channel(db: Session, channel: ChannelCreate, staff_id: int):
    print(channel.json())
    db_channel = models.Channel(name=channel.name, description=channel.description, department=channel.department.value, created_by=staff_id)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel
