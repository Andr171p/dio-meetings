from typing import Union

import io
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from ..constants import SUPPORTED_AUDIO_FORMATS


class Meeting(BaseModel):
    meeting_id: UUID = Field(default_factory=uuid4)  # Уникальный ID встречи
    audio_record: Union[io.BytesIO, bytes]  # Аудио запись встречи / совещания
    audio_format: str  # Формат аудио из возможных поддерживаемых

    @field_validator("audio_format")
    def validate_audio_format(cls, audio_format: str) -> str:
        if audio_format not in SUPPORTED_AUDIO_FORMATS:
            raise ValueError("Unsupported audio format")
        return audio_format
