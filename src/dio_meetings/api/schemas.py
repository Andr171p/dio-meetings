from typing import Annotated, Literal, Optional

from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field

from fastapi import UploadFile, File, Form


AudioFile = Annotated[UploadFile, File(..., description="Аудио запись встречи/совещания")]

TitleForm = Annotated[str, Form(..., description="Тема/название совещания")]

ParticipantsForm = Annotated[list[str], Form(..., description="Список участников встречи")]


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
