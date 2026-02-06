from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from ..database import repository
from ..database.base import session_factory
from ..schemas import Task

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get(
    path="/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=Task,
    summary="Получение статуса задачи"
)
async def get_task(task_id: UUID) -> Task:
    async with session_factory() as session:
        task = await repository.get_task(session, task_id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task not found by id {task_id}"
            )
    return task
