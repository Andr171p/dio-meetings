from typing import Optional

from uuid import UUID

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import TaskOrm
from ...core.base import TaskRepository
from ...core.dto import TaskCreate, CreatedTask


class SQLTaskRepository(TaskRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def create(self, task: TaskCreate) -> CreatedTask:
        async with self.session_factory() as session:
            stmt = (
                insert(TaskOrm)
                .values(**task.model_dump())
                .returning(TaskOrm.task_id)
            )
            result = await session.execute(stmt)
            await session.commit()
        created_task = result.scalar_one()
        return CreatedTask.model_validate(created_task)

    async def read(self, task_id: UUID) -> Optional[CreatedTask]:
        async with self.session_factory() as session:
            stmt = (
                select(TaskOrm)
                .where(TaskOrm.task_id == task_id)
            )
            result = await session.execute(stmt)
        task = result.scalar_one_or_none()
        return CreatedTask.model_validate(task) if task else None

    async def update(self, task_id: UUID, **kwargs) -> CreatedTask:
        async with self.session_factory() as session:
            stmt = (
                update(TaskOrm)
                .where(TaskOrm.task_id == task_id)
                .values(**kwargs)
                .returning(TaskOrm)
            )
            result = await session.execute(stmt)
            await session.commit()
        task = result.scalar_one()
        return CreatedTask.model_validate(task)

    async def delete(self, task_id: UUID) -> bool:
        async with self.session_factory() as session:
            stmt = (
                delete(TaskOrm)
                .where(TaskOrm.task_id == task_id)
            )
            result = await session.execute(stmt)
            await session.commit()
        return result.rowcount() > 0
