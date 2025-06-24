from uuid import UUID
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from .base import Base


class FileMetadataOrm(Base):
    __tablename__ = "file_metadata"

    key: Mapped[str]
    bucket: Mapped[str]
    size: Mapped[float]
    format: Mapped[str]
    type: Mapped[str]
    uploaded_date: Mapped[datetime] = mapped_column(DateTime)


class TaskOrm(Base):
    __tablename__ = "tasks"

    file_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True))
    status: Mapped[str]
    result_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    __table_args__ = (
        CheckConstraint("status IN ('NEW', 'RUNNING', 'DONE', 'ERROR')", "check_status"),
    )
