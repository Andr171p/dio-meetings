from uuid import UUID

from fastapi import APIRouter, status


tasks_router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)


@tasks_router.get(
    path="/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=...
)
async def get_task(task_id: UUID) -> ...:
    ...
