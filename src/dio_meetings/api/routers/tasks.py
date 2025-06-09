from uuid import UUID

from fastapi import APIRouter, status, HTTPException

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ...core.dto import CreatedTask, TaskCreate
from ...core.base import TaskRepository, MessageBroker

from ..params import TaskCreateSchema


tasks_router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
    route_class=DishkaRoute
)


@tasks_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreatedTask
)
async def create_task(
        task: TaskCreateSchema,
        task_repository: FromDishka[TaskRepository],
        broker: FromDishka[MessageBroker]
) -> CreatedTask:
    task = TaskCreate(meeting_key=task.meeting_key, status="RUNNING")
    created_task = await task_repository.create(task)
    if not created_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while creating task"
        )
    created_task.status = "NEW"
    await broker.publish(created_task, queue="tasks")
    return created_task


@tasks_router.get(
    path="/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=CreatedTask
)
async def get_task(task_id: UUID, task_repository: FromDishka[TaskRepository]) -> CreatedTask:
    task = await task_repository.read(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task
