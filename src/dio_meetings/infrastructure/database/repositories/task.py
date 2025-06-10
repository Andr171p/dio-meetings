from typing import Optional

import logging
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete

from ..models import TaskOrm

from src.dio_meetings.core.base import TaskRepository
from src.dio_meetings.core.dto import TaskCreate, CreatedTask
from src.dio_meetings.core.exceptions import (
    CreateDataError,
    ReadDataError,
    UpdateDataError,
    DeleteDataError
)


class SQLTaskRepository(TaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = session

    async def create(self, task: TaskCreate) -> CreatedTask:
        try:
            stmt = (
                insert(TaskOrm)
                .values(**task.model_dump())
                .returning(TaskOrm)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            created_task = result.scalar_one()
            return CreatedTask.model_validate(created_task)
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while creating task: {e}")
            raise CreateDataError(f"Error while creating task: {e}") from e

    async def read(self, task_id: UUID) -> Optional[CreatedTask]:
        try:
            stmt = (
                select(TaskOrm)
                .where(TaskOrm.task_id == task_id)
            )
            result = await self.session.execute(stmt)
            task = result.scalar_one_or_none()
            return CreatedTask.model_validate(task) if task else None
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while reading task: {e}")
            raise ReadDataError(f"Error while reading task: {e}") from e

    async def update(self, task_id: UUID, **kwargs) -> CreatedTask:
        try:
            stmt = (
                update(TaskOrm)
                .where(TaskOrm.task_id == task_id)
                .values(**kwargs)
                .returning(TaskOrm)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            task = result.scalar_one()
            return CreatedTask.model_validate(task)
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while updating task: {e}")
            raise UpdateDataError(f"Error while updating task: {e}") from e

    async def delete(self, task_id: UUID) -> bool:
        try:
            stmt = (
                delete(TaskOrm)
                .where(TaskOrm.task_id == task_id)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount() > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while deleting task: {e}")
            raise DeleteDataError(f"Error while deleting task: {e}") from e
