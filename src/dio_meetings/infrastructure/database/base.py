from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
