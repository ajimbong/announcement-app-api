from sqlalchemy.orm import Session

from api.db.models import ChannelPermission
from api.schemas.permission import PermissionCreate, PermissionUpdate


def get_permissions_for_channel(db: Session, channel_id: int):
    return db.query(ChannelPermission).filter(ChannelPermission.channel_id == channel_id).all()


def get_permissions_for_staff(db: Session, staff_id: int):
    return db.query(ChannelPermission).filter(ChannelPermission.staff_id == staff_id).all()


def get_permission_for_channel_and_staff(db: Session, channel_id: int, staff_id: int):
    return db.query(ChannelPermission).filter(ChannelPermission.channel_id == channel_id, ChannelPermission.staff_id == staff_id).first()


def add_permission(db: Session, permission: PermissionCreate):
    db_permission: ChannelPermission = ChannelPermission(
        channel_id=permission.channel_id,
        staff_id=permission.staff_id,
        access_level=permission.access_level.value
    )

    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def update_permission(db: Session, permission: PermissionUpdate):
    channel_id = permission.channel_id
    staff_id = permission.staff_id
    db_permission: ChannelPermission = db.query(ChannelPermission).filter(ChannelPermission.channel_id == channel_id, ChannelPermission.staff_id == staff_id).first()

    db_permission.access_level = permission.access_level.value
    db.commit()
    db.refresh(db_permission)
    return db_permission


def delete_permission(db: Session, channel_id: int, staff_id: int):
    db_permission: ChannelPermission = db.query(ChannelPermission).filter(ChannelPermission.channel_id == channel_id, ChannelPermission.staff_id == staff_id).first()

    db.delete(db_permission)
    db.commit()
