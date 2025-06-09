from typing import Literal

import io
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from .domain import Task
from ..constants import TASK_STATUS


ROLE = Literal[
    "system",
    "user",
    "ai"
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


class AIMessage(BaseMessage):
    role: ROLE = "ai"


class Transcription(BaseModel):
    text: str  # Транскрибированный текст
    speaker_id: int  # ID спикера
    emotion: EMOTION  # Эмоция спикера


class BuiltDocument(BaseModel):
    document_name: str
    file_data: bytes

    @classmethod
    def from_bytes_io(cls, document_name: str, file_buffer: io.BytesIO) -> "BuiltDocument":
        return cls(
            document_name=document_name,
            file_data=file_buffer.getvalue()
        )


class UploadedMeeting(BaseModel):
    meeting_key: str
    created_at: datetime = Field(default_factory=datetime.now)


class TaskCreate(BaseModel):
    meeting_key: str
    status: TASK_STATUS = "RUNNING"


class CreatedTask(Task):
    created_at: datetime
