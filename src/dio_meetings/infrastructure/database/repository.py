from typing import Optional

from uuid import UUID

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import TaskOrm
from ...core.base import TaskRepository
from ...core.domain import Task
from ...core.dto import TaskCreate, TaskRead


class SQLTaskRepository(TaskRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def create(self, task: TaskCreate) -> TaskRead:
        async with self.session_factory() as session:
            stmt = (
                insert(TaskOrm)
                .values(**task.model_dump())
                .returning(TaskOrm)
            )
            result = await session.execute(stmt)
            await session.commit()
        created_task = result.scalar_one()
        return TaskRead.model_validate(created_task)

    async def read(self, task_id: UUID) -> Optional[TaskRead]:
        async with self.session_factory() as session:
            stmt = (
                select(TaskOrm)
                .where(TaskOrm.task_id == task_id)
            )
            result = await session.execute(stmt)
        task = result.scalar_one_or_none()
        return TaskRead.model_validate(task) if task else None

    async def update(self, task: Task) -> TaskRead:
        async with self.session_factory() as session:
            stmt = (
                update(TaskOrm)
                .where(TaskOrm.task_id == task.task_id)
                .values(**task.model_dump(exclude={"task_id"}))
                .returning(TaskOrm)
            )
            result = await session.execute(stmt)
            await session.commit()
        task = result.scalar_one()
        return TaskRead.model_validate(task)

    async def delete(self, task_id: UUID) -> bool:
        async with self.session_factory() as session:
            stmt = (
                delete(TaskOrm)
                .where(TaskOrm.task_id == task_id)
            )
            result = await session.execute(stmt)
            await session.commit()
        return result.rowcount() > 0
