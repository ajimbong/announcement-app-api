from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from enums import Role, Department

from .database import Base


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role))
    created_by = Column(Integer, ForeignKey("staff.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    department = Column(Enum(Department), nullable=False)
    created_by = Column(Integer, ForeignKey("staff.id"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    staff_created = relationship("Staff", back_populates="channel")