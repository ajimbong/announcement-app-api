from sqlalchemy.orm import Session

from api.db import models
from api.db.models import Channel
from api.schemas.channel import ChannelCreate, ChannelUpdate


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


def update_channel(db: Session, channel: ChannelUpdate, channel_id: int):
    db_channel: Channel = db.query(Channel).filter(Channel.id==channel_id).first()

    db_channel.name = channel.name
    db_channel.description = channel.description
    db_channel.department = channel.department.value
    db_channel.created_by = channel.created_by
    db.commit()
    db.refresh(db_channel)
    return db_channel


def delete_channel(db: Session, channel_id: int):
    db_channel: Channel = db.query(Channel).filter_by(id=channel_id).first()

    db.delete(db_channel)
    db.commit()
