import io
from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .enums import Role, TaskStatus, Emotion
from .domain import Task, Meeting, Result


class BaseMessage(BaseModel):
    role: Role
    text: str


class SystemMessage(BaseMessage):
    role: Role = Role.SYSTEM


class UserMessage(BaseMessage):
    role: Role = Role.USER


class AIMessage(BaseMessage):
    role: Role = Role.AI


class Transcription(BaseModel):
    text: str         # Транскрибированный текст
    speaker_id: int   # ID спикера
    emotion: Emotion  # Эмоция спикера

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
    status: TaskStatus = TaskStatus.NEW


class CreatedTask(Task):
    created_at: datetime
    updated_at: datetime


class CreatedResult(Result):
    created_at: datetime
