from enum import StrEnum


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    AI = "ai"


class Emotion(StrEnum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class TaskStatus(StrEnum):
    NEW = "NEW"
    RUNNING = "RUNNING"
    DONE = "DONE"
    ERROR = "ERROR"


class FileType(StrEnum):
    AUDIO = "AUDIO"
    DOCUMENT = "DOCUMENT"
