from typing import Literal

from pydantic import BaseModel


ROLE = Literal[
    "system",
    "user",
    "assistant"
]


EMOTION = Literal[
    "positive",
    "neutral",
    "negative"
]


class BaseMessage(BaseModel):
    role: ROLE
    text: str


class SystemMessage(BaseMessage):
    role: ROLE = "system"


class UserMessage(BaseMessage):
    role: ROLE = "user"


class AssistantMessage(BaseMessage):
    role: ROLE = "assistant"


class Transcription(BaseModel):
    text: str  # Транскрибированный текст
    speaker_id: int  # ID спикера
    emotion: EMOTION  # Эмоция спикера


class UploadMeeting(BaseModel):
    name: str
    file_path: str
