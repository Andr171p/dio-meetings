from typing import Literal

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeFloat,
    PositiveFloat,
    PositiveInt,
)

from .utils import current_datetime


class Meeting(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=current_datetime)
    original_filename: str
    content_type: Literal["audio", "video"]
    s3_key: str
    format: str
    size_mb: PositiveFloat
    duration: PositiveFloat


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=current_datetime)
    meeting_id: UUID
    status: Literal[
        "pending",
        "processing",
        "transcribing",
        "generating",
        "complete",
        "failed"
    ] = Field(default="pending")
    error_message: str | None = None


class Transcript(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    meeting_id: UUID
    full_text: str
    word_count: PositiveInt
    start_time: NonNegativeFloat
    end_time: NonNegativeFloat
    duration: PositiveFloat


class Minutes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=current_datetime)
    meeting_id: UUID
    title: str
    md_text: str
