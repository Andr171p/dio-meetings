from typing import Any, Literal, Optional, Union

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from .constants import EMOTIONS


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
    emotion: EMOTIONS

    @classmethod
    def from_response(cls, response: dict[str, Any]) -> "RecognizedResult":
        return cls(
            text=response["results"][0]["normalized_text"],
            speaker_id=response["speaker_info"]["speaker_id"],
            emotion=cls._get_emotion(response["emotions_result"])
        )

    @staticmethod
    def _get_emotion(emotions: dict[EMOTIONS, float]) -> EMOTIONS:
        return max(emotions.items(), key=lambda x: x[1])[0]
