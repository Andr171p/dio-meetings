from typing import Literal, Optional

from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field

from fastapi import File


class UploadMeeting(BaseModel):
    title: str  # Название встречи (оглавление)
    participants: list[str]  # ФИО участников встречи
    audio_file: File  # Аудио файл с записью встречи


STATUS = Literal[
    "NEW",  # Новое совещание
    "PROCESS",  # В процессе составления протокола
    "DONE",  # Протокол составлен
    "ERROR"  # Ошибка при составлении протокола
]


class AcceptedMeeting(BaseModel):
    meeting_id: UUID = Field(default_factory=uuid4)  # ID задачи на составление протокола
    status:  STATUS = "NEW"
    created_at: datetime = Field(default_factory=datetime.now)  # Дата создания задачи


class MeetingStatus(BaseModel):
    status: STATUS
    meeting_id: UUID
    protocol_id: Optional[UUID]  # ID сформированного протокола встречи


class ComposedProtocol(BaseModel):
    title: str  # Название
    text: str  # Текст протокола в формате Markdown
    file: File  # Word файл протокола
