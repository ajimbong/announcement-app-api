from sqlalchemy.orm import Session

from api.db.models import Announcement
from api.schemas.announcement import AnnouncementCreate, AnnouncementUpdate


"""
- Get Announcements belonging to a channel
- Get the details of an announcement
- Create a new announcement
- Update an existing announcement
- Delete an existing announcement
"""


def get_announcements(db: Session, channel_id: int):
    return db.query(Announcement).filter_by(channel_id=channel_id).all()


def get_announcement(db: Session, announcement_id: int):
    return db.query(Announcement).filter(Announcement.id == announcement_id).first()


def create_announcement(db: Session, announcement: AnnouncementCreate):
    db_announcement: Announcement = Announcement(
        message=announcement.message,
        channel_id=announcement.channel_id,
        staff_id=announcement.staff_id
    )

    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement


def update_announcement(db: Session, announcement: AnnouncementUpdate, announcement_id: int):
    db_announcement: Announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()

    db_announcement.message = announcement.message
    db_announcement.channel_id = announcement.channel_id
    db_announcement.staff_id = announcement.staff_id

    db.commit()
    db.refresh(db_announcement)
    return db_announcement


def delete_announcement(db: Session, ann_id: int):
    db_announcement: Announcement = db.query(Announcement).filter(Announcement.id == ann_id).first()

    db.delete(db_announcement)
    db.commit()
