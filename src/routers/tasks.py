from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.repositories import TaskRepository
from ..dependencies import get_db
from ..schemas import Task
from ..service import create_task

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    path="",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Task,
    summary="Создание задачи на генерацию протокола",
)
async def create(meeting_id: UUID = Body(..., embed=True)) -> Task:
    return await create_task(meeting_id)


@router.get(
    path="/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=Task,
    summary="Получение текущей задачи"
)
async def get(task_id: UUID, session: AsyncSession = Depends(get_db)) -> Task:
    repository = TaskRepository(session)
    task = await repository.read(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    return task
