from uuid import UUID

from fastapi import APIRouter, status, HTTPException

from dishka.integrations.fastapi import DishkaRoute, FromDishka as Depends

from ..schemas import TaskCreateSchema

from ...core.domain import Task
from ...core.services import TaskService

from ...constants import NOT_FOUND, NOT_CREATED

tasks_router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
    route_class=DishkaRoute
)


@tasks_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=Task,
    summary="Создаёт задачу на генерацию протокола совещания."
)
async def create_task(task_create: TaskCreateSchema, task_service: Depends[TaskService]) -> Task:
    created_task = await task_service.create(task_create.file_id)
    if not created_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=NOT_CREATED
        )
    return created_task


@tasks_router.get(
    path="/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=Task,
    summary="Получает статус текущей задачи."
)
async def get_task_status(task_id: UUID, task_service: Depends[TaskService]) -> Task:
    task = await task_service.get_status(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return task
