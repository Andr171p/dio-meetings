from uuid import UUID

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from sqlalchemy import select

from ..database import models
from ..database.base import session_factory
from ..schemas import MeetingMinutes, Task
from ..services.tasks import create_task

router = APIRouter(prefix="/meeting-minutes", tags=["Minutes of meeting"])

SUPPORTED_AUDIO_FORMATS = {"wav", "mp3", "m4a", "ogg", "flac"}


@router.post(
    path="/generate",
    status_code=status.HTTP_201_CREATED,
    response_model=Task,
    summary="Создание задачи на генерацию протокола"
)
async def create_generation_task(audio_file: UploadFile = File(...)) -> Task:
    content = await audio_file.read()
    filename = audio_file.filename
    if filename.split(".")[-1] not in SUPPORTED_AUDIO_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported audio format: {filename.split('.')[-1]}!"
        )
    return await create_task(content, filename)


@router.post(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=MeetingMinutes,
    summary="Получение протокола совещания"
)
async def get_meeting_minutes(task_id: UUID = Query(...)) -> MeetingMinutes:
    async with session_factory() as session:
        stmt = (
            select(models.MeetingMinutes)
            .where(models.MeetingMinutes.task_id == task_id)
        )
        result = await session.execute(stmt)
        model = await result.scalar_one_or_none()
        if model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )
    return MeetingMinutes.model_validate(model)
