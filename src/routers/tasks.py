from uuid import UUID

from fastapi import Body, Depends, HTTPException, status
from faststream.redis import RedisBroker, fastapi

from ..database.repositories import TaskRepository
from ..dependencies import get_task_processor, get_task_repo
from ..schemas import Task
from ..services.task_processing import TaskProcessor
from ..settings import settings

router = fastapi.RedisRouter(url=settings.redis.url, prefix="/tasks", tags=["Tasks"])


def get_broker() -> RedisBroker:
    return router.broker


@router.post(
    path="",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Task,
    summary="Создание задачи на генерацию протокола",
)
async def create_task(
        meeting_id: UUID = Body(..., embed=True),
        repository: TaskRepository = Depends(get_task_repo),
        broker: RedisBroker = Depends(get_broker),
) -> Task:
    task = Task(meeting_id=meeting_id)
    await repository.create(task)
    await broker.publish(str(task.id), channel="meeting:minutes:generate")
    return task


@router.get(
    path="/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=Task,
    summary="Получение текущей задачи"
)
async def get_task(task_id: UUID, repository: TaskRepository = Depends(get_task_repo)) -> Task:
    task = await repository.read(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TASK_NOT_FOUND")
    return task


@router.subscriber("meeting:minutes:generate")
async def process_task(
        task_id: str, processor: TaskProcessor = Depends(get_task_processor)
) -> None:
    await processor.process(UUID(task_id))
