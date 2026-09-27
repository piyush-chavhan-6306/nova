from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    ORGANIZER = "ORGANIZER"
    JUDGE = "JUDGE"
    PARTICIPANT = "PARTICIPANT"


class HackathonStatus(str, Enum):
    DRAFT = "DRAFT"
    UPCOMING = "UPCOMING"
    REGISTRATION_OPEN = "REGISTRATION_OPEN"
    ACTIVE = "ACTIVE"
    SUBMISSIONS_CLOSED = "SUBMISSIONS_CLOSED"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


class TeamRole(str, Enum):
    LEAD = "LEAD"
    MEMBER = "MEMBER"


class InvitationStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    EXPIRED = "EXPIRED"


class SubmissionStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    LOCKED = "LOCKED"


class ReviewStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUBMITTED = "SUBMITTED"
    LOCKED = "LOCKED"


class RegistrationStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
