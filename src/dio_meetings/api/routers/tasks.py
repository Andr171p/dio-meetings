from uuid import UUID

from fastapi import APIRouter, status

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ...core.domain import Task
from ...core.base import MessageBroker


tasks_router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
    route_class=DishkaRoute
)


@tasks_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=...
)
async def create_task(task: Task, broker: FromDishka[MessageBroker]) -> ...:
    ...


@tasks_router.get(
    path="/{task_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=...
)
async def get_task_status(task_id: UUID) -> ...:
    ...
