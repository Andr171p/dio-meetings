from typing import Any, Literal, Optional, Union

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class TaskResult(BaseModel):
    """Результат созданной задачи"""
    id: Union[UUID, str]  # Идентификатор задачи
    created_at: datetime  # Дата создания задачи
    updated_at: datetime  # Дата обновления статуса задачи
    status: Literal[
        "NEW",
        "RUNNING",
        "CANCELED",
        "DONE",
        "ERROR"
    ]  # статус задачи


class FinishedTaskResult(BaseModel):
    """Результат законченной задачи"""
    id: Union[UUID, str]  # Идентификатор задачи
    created_at: datetime  # Дата создания задачи
    updated_at: datetime  # Дата обновления статуса задачи
    status: Literal[
        "NEW",
        "RUNNING",
        "CANCELED",
        "DONE",
        "ERROR"
    ]  # статус задачи
    response_file_id: UUID


class RecognizedResult(BaseModel):
    """Результат распознавания части аудио"""
    text: str
    speaker_id: Optional[int]
    emotion: Literal[
        "positive",
        "neutral",
        "negative"
    ]

    @classmethod
    def from_response(cls, response: dict[str, Any]) -> "RecognizedResult":
        ...
