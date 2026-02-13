from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import repositories
from .database.base import session_factory
from .services.meeting_media import MeetingMediaService
from .services.task_processing import TaskProcessor


async def get_db() -> AsyncSession:
    async with session_factory() as session:
        yield session


def get_meeting_repo(session: AsyncSession = Depends(get_db)) -> repositories.MeetingRepository:
    return repositories.MeetingRepository(session)


def get_task_repo(session: AsyncSession = Depends(get_db)) -> repositories.TaskRepository:
    return repositories.TaskRepository(session)


def get_transcript_repo(
        session: AsyncSession = Depends(get_db)
) -> repositories.TranscriptRepository:
    return repositories.TranscriptRepository(session)


def get_minutes_repo(
        session: AsyncSession = Depends(get_db)
) -> repositories.MinutesRepository:
    return repositories.MinutesRepository(session)


def get_meeting_media_service(
        repository: repositories.MeetingRepository = Depends(get_meeting_repo)
) -> MeetingMediaService:
    return MeetingMediaService(repository)


def get_task_processor(session: AsyncSession = Depends(get_db)) -> TaskProcessor:
    return TaskProcessor(
        meeting_repo=repositories.MeetingRepository(session),
        task_repo=repositories.TaskRepository(session),
        transcript_repo=repositories.TranscriptRepository(session),
        minutes_repo=repositories.MinutesRepository(session),
    )
