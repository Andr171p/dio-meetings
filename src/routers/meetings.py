from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.repositories import MeetingRepository
from ..dependencies import get_db
from ..schemas import Meeting
from ..service import delete_meeting, upload_meeting

router = APIRouter(prefix="/meetings", tags=["Meetings"])


@router.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=Meeting,
    summary="Загрузка записи встречи"
)
async def upload(meeting_file: UploadFile = File(...)) -> Meeting:
    return await upload_meeting(await meeting_file.read(), meeting_file.filename)


@router.get(
    path="/{meeting_id}",
    status_code=status.HTTP_200_OK,
    response_model=Meeting,
    summary="Получение информации о встрече"
)
async def get(meeting_id: UUID, session: AsyncSession = Depends(get_db)) -> Meeting:
    repository = MeetingRepository(session)
    meeting = await repository.read(meeting_id)
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    return meeting


@router.delete(
    path="/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление встречи",
)
async def delete(meeting_id: UUID) -> None:
    return await delete_meeting(meeting_id)
