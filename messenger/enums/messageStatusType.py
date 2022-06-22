from enum import Enum


class MessageStatusType(str, Enum):
    sent = "sent"
    read = "read"
