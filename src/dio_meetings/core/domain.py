from typing import Optional

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..constants import TASK_STATUS


class Meeting(BaseModel):
    meeting_id: UUID  # Уникальный ID встречи
    name: str  # Название встречи
    audio_format: str  # Формат аудио файла
    duration: float  # Продолжительность в секундах
    speakers_count: int  # Количество участников
    file_name: str  # Ключ к файлу из s3 хранилища, в формате [uuid].[audio_format]
    date: datetime  # Дата встречи

    model_config = ConfigDict(from_attributes=True)


class Task(BaseModel):
    task_id: UUID
    meeting_id: UUID
    status: TASK_STATUS  # Статус выполнения задачи
    result_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Result(BaseModel):
    result_id: UUID
    file_name: str

    model_config = ConfigDict(from_attributes=True)
