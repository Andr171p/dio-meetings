from typing import Literal

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
)

from .utils import current_datetime


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=current_datetime)
    filename: str
    audio_s3_key: str
    status: Literal[
        "pending",
        "processing",
        "complete",
        "failed"
    ] = Field(default="pending")
    error_message: str | None = None


class AudioChunk(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    index: NonNegativeInt
    total_count: PositiveInt
    content: bytes
    audio_format: str
    size_mb: PositiveFloat
    duration_ms: PositiveInt


class MeetingMinutes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=current_datetime)
    task_id: UUID
    transcript: str
    summary: str
    audio_s3_key: str
