from api.schemas.announcement import Announcement
from api.schemas.channel import Channel
from api.schemas.staff import Staff
from api.schemas.student import Student
from api.schemas.subscription import Subscription
from api.schemas.permission import Permission


class StaffExtra(Staff):
    channels: list[Channel]


class ChannelExtra(Channel):
    staff_created: Staff


class SubscriptionExtra(Subscription):
    channel: Channel
    student: Student


class StudentExtra(Student):
    subscriptions: list[Subscription]


class AnnouncementExtra(Announcement):
    channel: Channel
    staff: Staff


class PermissionExtra(Permission):
    channel: Channel
    staff: Staff
