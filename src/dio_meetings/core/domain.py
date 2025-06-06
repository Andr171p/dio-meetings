from typing import Optional, Union

import io
from uuid import UUID

from pydantic import BaseModel, field_validator

from ..constants import SUPPORTED_AUDIO_FORMATS, TASK_STATUS


class Meeting(BaseModel):
    meeting_key: str  # Уникальный ID ключ совещания в формате {uuid}.{audio_format}
    audio_record: Union[io.BytesIO, bytes]  # Аудио запись встречи / совещания
    audio_format: str  # Формат аудио из возможных поддерживаемых

    @field_validator("audio_format")
    def validate_audio_format(cls, audio_format: str) -> str:
        if audio_format not in SUPPORTED_AUDIO_FORMATS:
            raise ValueError("Unsupported audio format")
        return audio_format


class Task(BaseModel):
    task_id: UUID
    meeting_key: str
    status: TASK_STATUS  # Статус выполнения задачи
    protocol_key: Optional[str] = None
