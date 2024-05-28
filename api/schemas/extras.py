from api.schemas.channel import Channel
from api.schemas.staff import Staff
from api.schemas.student import Student
from api.schemas.subscription import Subscription


class StaffExtra(Staff):
    channels: list[Channel]


class ChannelExtra(Channel):
    staff_created: Staff


class SubscriptionExtra(Subscription):
    channel: Channel
    student: Student


class StudentExtra(Student):
    subscriptions: list[Subscription]