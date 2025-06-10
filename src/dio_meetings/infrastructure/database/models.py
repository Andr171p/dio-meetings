from uuid import UUID
from datetime import datetime

from sqlalchemy import CheckConstraint, text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from .base import Base


class MeetingOrm(Base):
    __tablename__ = "meetings"

    meeting_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    name: Mapped[str]
    audio_format: Mapped[str]
    duration: Mapped[float]
    speakers_count: Mapped[int]
    file_name: Mapped[str] = mapped_column(unique=True)
    date: Mapped[datetime] = mapped_column(DateTime)


class TaskOrm(Base):
    __tablename__ = "tasks"

    task_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=text("gen_random_uuid()")
    )
    meeting_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True))
    status: Mapped[str]
    result_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        unique=True,
        nullable=True
    )

    result: Mapped["ResultOrm"] = relationship(back_populates="task")

    __table_args__ = (
        CheckConstraint("status IN ('NEW', 'RUNNING', 'DONE', 'ERROR')", "check_status"),
    )


class ResultOrm(Base):
    __tablename__ = "results"

    result_id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.result_id"),
        unique=True,
        nullable=True
    )
    file_name: Mapped[str] = mapped_column(nullable=False)

    task: Mapped["TaskOrm"] = relationship(
        argument="TaskOrm",
        back_populates="result"
    )
