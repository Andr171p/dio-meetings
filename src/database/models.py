from uuid import UUID

from sqlalchemy import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Meeting(Base):
    __tablename__ = "meetings"

    original_filename: Mapped[str]
    content_type: Mapped[str]
    s3_key: Mapped[str] = mapped_column(unique=True)
    format: Mapped[str]
    size_mb: Mapped[float]
    duration: Mapped[float]


class Task(Base):
    __tablename__ = "tasks"

    meeting_id: Mapped[UUID]
    status: Mapped[str]
    error_message: Mapped[str | None] = mapped_column(nullable=True)


class Transcript(Base):
    __tablename__ = "transcripts"

    meeting_id: Mapped[UUID]
    full_text: Mapped[str] = mapped_column(TEXT)
    word_count: Mapped[int]
    start_time: Mapped[float]
    end_time: Mapped[float]
    duration: Mapped[float]


class Minutes(Base):
    __tablename__ = "minutes"

    task_id: Mapped[UUID] = mapped_column(unique=True)
    transcript: Mapped[str] = mapped_column(TEXT)
    summary: Mapped[str] = mapped_column(TEXT)
    audio_s3_key: Mapped[str] = mapped_column(unique=True)
