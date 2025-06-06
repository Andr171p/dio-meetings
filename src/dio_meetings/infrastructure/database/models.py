from uuid import UUID

from sqlalchemy import CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from .base import Base



class TaskOrm(Base):
    __tablename__ = "tasks"

    task_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    meeting_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True))
    status: Mapped[str]
    protocol_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    __table_args__ = (
        CheckConstraint("status IN ('NEW', 'RUNNING', 'DONE', 'ERROR')", "check_status"),
    )

    def __str__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"task_id={self.task_id}, "
                f"status={self.status}, "
                f"protocol_id={self.protocol_id}, "
                f"created_at={self.created_at})")

    def __repr__(self) -> str:
        return str(self)
