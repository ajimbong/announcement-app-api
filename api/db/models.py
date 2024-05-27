from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    matricule: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), onupdate=datetime.now())

    subscriptions: Mapped[List["StudentSubscription"]] = relationship(back_populates="student")

    def __repr__(self):
        return f"<Student id={self.id}, name={self.name}, email={self.email}, matricule={self.matricule}>"


class Staff(Base):
    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str]
    created_by: Mapped[int] = mapped_column(ForeignKey("staff.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    channels: Mapped[List["Channel"]] = relationship(back_populates="staff_created")
    announcements: Mapped[List["Announcement"]] = relationship(back_populates="staff")
    channel_permissions: Mapped[List["ChannelPermission"]] = relationship(back_populates="staff")

    def __repr__(self):
        return f"<User id={self.id}, name={self.name}, email={self.email}, role={self.role}>"


class Channel(Base):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text)
    department: Mapped[str] = mapped_column(nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("staff.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    staff_created: Mapped["Staff"] = relationship(back_populates="channels")
    announcements: Mapped[List["Announcement"]] = relationship(back_populates="channel")
    subscriptions: Mapped[List["StudentSubscription"]] = relationship(back_populates="channel")
    permissions: Mapped["ChannelPermission"] = relationship(back_populates="channel")

    def __repr__(self):
        return f"<Channel id={self.id}, name={self.name} >"


class Announcement(Base):
    __tablename__ = "announcement"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"), nullable=False)
    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), onupdate=datetime.now())

    channel: Mapped["Channel"] = relationship(back_populates="announcements")
    staff: Mapped["Staff"] = relationship(back_populates="announcements")

    def __repr__(self):
        return f"<Announcement id={self.id}, message='{self.message[:50]}...', channel_id={self.channel_id}, staff_id={self.staff_id}>"

class ChannelPermission(Base):
    __tablename__ = "channel_permission"

    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"), primary_key=True)
    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.id"), primary_key=True)
    access_level: Mapped[str] = mapped_column(default="READ")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), onupdate=datetime.now())

    channel: Mapped["Channel"] = relationship(back_populates="permissions")
    staff: Mapped["Staff"] = relationship(back_populates="channel_permissions")

    def __repr__(self):
        return f"<ChannelPermission channel_id={self.channel_id}, staff_id={self.staff_id}, access_level={self.access_level}>"

class StudentSubscription(Base):
    __tablename__ = "student_subscription"

    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"), primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    channel: Mapped["Channel"] = relationship(back_populates="subscriptions")
    student: Mapped["Student"] = relationship(back_populates="subscriptions")

    def __repr__(self):
        return f"<StudentSubscription channel_id={self.channel_id}, student_id={self.student_id}>"
