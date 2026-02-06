from uuid import UUID

from sqlalchemy import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Task(Base):
    __tablename__ = "tasks"

    filename: Mapped[str]
    audio_s3_key: Mapped[str] = mapped_column(unique=True)
    status: Mapped[str]
    error_message: Mapped[str | None] = mapped_column(nullable=True)


class MeetingMinutes(Base):
    __tablename__ = "meeting_minutes"

    task_id: Mapped[UUID] = mapped_column(unique=True)
    transcript: Mapped[str] = mapped_column(TEXT)
    summary: Mapped[str] = mapped_column(TEXT)
    audio_s3_key: Mapped[str] = mapped_column(unique=True)
