from typing import Literal

import io
from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .domain import Task, Meeting, Result

from ..constants import TASK_STATUS, EMOTION


ROLE = Literal[
    "system",
    "user",
    "ai"
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

    model_config = ConfigDict(from_attributes=True)


class Document(BaseModel):
    id: UUID
    file_name: str
    file_data: bytes

    @classmethod
    def from_bytes_io(cls, file_buffer: io.BytesIO, file_format: str) -> "Document":
        id = uuid4()
        return cls(
            id=id,
            file_name=f"{id}.{file_format}",
            file_data=file_buffer.getvalue()
        )


class MeetingUpload(BaseModel):
    name: str
    file_name: str
    speakers_count: int
    audio_bytes: bytes


class CreatedMeeting(Meeting):
    meeting_id: UUID
    created_at: datetime


class DownloadedFile(BaseModel):
    file_data: bytes
    file_name: str


class TaskCreate(BaseModel):
    meeting_id: UUID
    status: TASK_STATUS = "RUNNING"


class CreatedTask(Task):
    created_at: datetime
    updated_at: datetime


class CreatedResult(Result):
    created_at: datetime
