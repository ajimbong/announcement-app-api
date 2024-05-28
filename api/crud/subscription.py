from sqlalchemy.orm import Session

from api.db.models import StudentSubscription as Subscription
from api.schemas.subscription import SubscriptionCreate


def get_subscriptions_for_channel(db: Session, channel_id: int):
    return db.query(Subscription).filter(Subscription.channel_id == channel_id).all()


def get_subscriptions_for_student(db: Session, student_id: int):
    return db.query(Subscription).filter(Subscription.student_id == student_id).all()


def get_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Subscription).offset(skip).limit(limit).all()


def get_sub_by_channel_and_student(db: Session, channel_id: int, student_id: int):
    return db.query(Subscription).filter_by(channel_id=channel_id, student_id=student_id).all()


def subscribe(db: Session, subscription: SubscriptionCreate):
    db_subscription: Subscription = Subscription(
        channel_id=subscription.channel_id,
        student_id=subscription.student_id,
    )

    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def unsubscribe(db: Session, channel_id: int, student_id: int):
    db_subscription: Subscription = db.query(Subscription).filter_by(channel_id=channel_id, student_id=student_id).first()

    db.delete(db_subscription)
    db.commit()
