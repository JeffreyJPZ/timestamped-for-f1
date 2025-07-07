from enum import StrEnum


class EventCategoryEnum(StrEnum):
    CAR_ACTION = "car-action"
    CAR_NOTIFICATION = "car-notification"
    SECTOR_NOTIFICATION = "sector-notification"
    TRACK_NOTIFICATION = "track-notificiation"
    INCIDENT_NOTIFICATION = "incident-notification"
    INCIDENT_VERDICT = "incident-verdict"
    SESSION_NEUTRALIZED = "session-neutralized"
    OTHER = "other"

# TODO: add more enums
class EventCauseEnum(StrEnum):
    OVERTAKE = "overtake"
    PIT = "pit"
    BLUE_FLAG = "blue-flag"
    BLACK_AND_WHITE_FLAG = "black-and-white-flag"
    BLACK_AND_ORANGE_FLAG = "black-and-orange-flag",
    BLACK_FLAG = "black-flag"
    GREEN_FLAG = "green-flag"
    YELLOW_FLAG = "yellow-flag"
    DOUBLE_YELLOW_FLAG = "double-yellow-flag"
    RED_FLAG = "red-flag"
    CHEQUERED_FLAG = "chequered-flag"
    SAFETY_CAR = "safety-car"
    VIRTUAL_SAFETY_CAR = "virtual-safety-car"