from typing import Optional

from uuid import UUID

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import TaskOrm

from src.dio_meetings.core.domain import Task
from src.dio_meetings.core.base import CRUDRepository
from src.dio_meetings.core.exceptions import (
    CreationError,
    ReadingError,
    UpdatingError,
    DeletingError
)


class SQLTaskRepository(CRUDRepository[Task]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, task: Task) -> Task:
        try:
            stmt = (
                insert(TaskOrm)
                .values(**task.model_dump(exclude_none=True))
                .returning(TaskOrm)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            created_task = result.scalar_one()
            return Task.model_validate(created_task)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise CreationError(f"Error while creating task: {e}") from e

    async def read(self, id: UUID) -> Optional[Task]:
        try:
            stmt = (
                select(TaskOrm)
                .where(TaskOrm.id == id)
            )
            result = await self.session.execute(stmt)
            task = result.scalar_one_or_none()
            return Task.model_validate(task) if task else None
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ReadingError(f"Error while reading task: {e}") from e

    async def update(self, id: UUID, **kwargs) -> Task:
        try:
            stmt = (
                update(TaskOrm)
                .values(**kwargs)
                .where(TaskOrm.id == id)
                .returning(TaskOrm)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            updated_task = result.scalar_one()
            return Task.model_validate(updated_task) if updated_task else None
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise UpdatingError(f"Error while updating task: {e}") from e

    async def delete(self, id: UUID) -> bool:
        try:
            stmt = (
                delete(TaskOrm)
                .where(TaskOrm.id == id)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DeletingError(f"Error while deleting task: {e}") from e
