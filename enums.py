from enum import Enum

class Role(Enum):
    LECTURER = 'lecturer'
    HOD = 'hod'
    SECRETORY = 'secretory'
    ADMINISTRATOR = 'administrator'
    OTHER = 'other'

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        return None


class Department(Enum):
    ENGINEERING = 'engineering'
    MANAGEMENT = 'management'
    COMMUNICATION = 'communication'
    HEALTH_SCIENCES = 'health_sciences'
    GENERAL = 'general'

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        return None