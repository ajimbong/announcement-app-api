from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base


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

    def __repr__(self):
        return f"<Channel id={self.id}, name={self.name} >"