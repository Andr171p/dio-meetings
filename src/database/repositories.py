from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from . import models
from .base import Base


class SqlAlchemyRepository[SchemaT: BaseModel, ModelT: Base]:
    schema: type[SchemaT]
    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, schema: SchemaT) -> None:
        stmt = insert(self.model).values(**schema.model_dump())
        await self.session.execute(stmt)
        await self.session.flush()
        await self.session.commit()

    async def read(self, id: UUID) -> SchemaT | None:  # noqa: A002
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return None if model is None else self.schema.model_validate(model)

    async def update(self, id: UUID, **kwargs) -> SchemaT | None:  # noqa: A002
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        model = result.scalar_one_or_none()
        return None if model is None else self.schema.model_validate(model)

    async def delete(self, id: UUID) -> None:  # noqa: A002
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)
        await self.session.commit()


class MeetingRepository(SqlAlchemyRepository[schemas.Meeting, models.Meeting]):
    schema = schemas.Meeting
    model = models.Meeting


class TaskRepository(SqlAlchemyRepository[schemas.Task, models.Task]):
    schema = schemas.Task
    model = models.Task


class TranscriptRepository(SqlAlchemyRepository[schemas.Transcript, models.Transcript]):
    schema = schemas.Transcript
    model = models.Transcript

    async def get_by_meeting(self, meeting_id: UUID) -> schemas.Transcript | None:
        stmt = select(self.model).where(self.model.meeting_id == meeting_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return None if model is None else self.schema.model_validate(model)


class MinutesRepository(SqlAlchemyRepository[schemas.Minutes, models.Minutes]):
    schema = schemas.Minutes
    model = models.Minutes

    async def get_by_meeting(self, meeting_id: UUID) -> schemas.Minutes | None:
        stmt = (
            select(self.model)
            .where(self.model.meeting_id == meeting_id)
            .order_by(self.model.created_at)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return None if model is None else self.schema.model_validate(model)
