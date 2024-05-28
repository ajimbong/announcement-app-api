from datetime import datetime

from pydantic import BaseModel


class SubscriptionBase(BaseModel):
    channel_id: int
    student_id: int


class SubscriptionCreate(SubscriptionBase):
    pass


class Subscription(SubscriptionBase):
    created_at: datetime

    class Config:
        from_attributes = True
