from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import MeetingMinutes, Task
from . import models


async def add_task(session: AsyncSession, task: Task) -> None:
    stmt = insert(models.Task).values(**task.model_dump())
    await session.execute(stmt)


async def get_task(session: AsyncSession, task_id: UUID) -> Task | None:
    stmt = select(models.Task).where(models.Task.id == task_id)
    result = await session.execute(stmt)
    model = result.scalar_one_or_none()
    return None if model is None else Task.model_validate(model)


async def update_task_status(
        session: AsyncSession, task_id: UUID, task_status: str
) -> Task:
    stmt = (
        update(models.Task)
        .where(models.Task.id == task_id)
        .values(task_status=task_status)
        .returning(models.Task)
    )
    result = await session.execute(stmt)
    model = result.scalar_one()
    return Task.model_validate(model)


async def add_meeting_minutes(
        session: AsyncSession, meeting_minutes: MeetingMinutes
) -> None:
    stmt = insert(models.MeetingMinutes).values(**meeting_minutes.model_dump())
    await session.execute(stmt)
