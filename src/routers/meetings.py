import logging
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from ..database.repositories import MeetingRepository, TranscriptRepository
from ..dependencies import get_meeting_media_service, get_meeting_repo, get_transcript_repo
from ..schemas import Meeting, MeetingResponse, MeetingUpdate, Transcript
from ..services.meeting_media import MeetingMediaService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/meetings", tags=["Meetings"])


@router.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=MeetingResponse,
    summary="Загрузка записи встречи"
)
async def upload_meeting(
        file: UploadFile = File(...),
        service: MeetingMediaService = Depends(get_meeting_media_service),
) -> MeetingResponse:
    logger.info("Starting reading client `%s` file, size %s bytes", file.filename, file.size)
    meeting = await service.upload_and_create(file)
    return MeetingResponse.model_validate(meeting)


@router.patch(
    path="/{meeting_id}",
    status_code=status.HTTP_200_OK,
    response_model=MeetingResponse,
    summary="Добавление дополнительной информации"
)
async def update_meeting(
        meeting_id: UUID,
        update: MeetingUpdate,
        repository: MeetingRepository = Depends(get_meeting_repo)
) -> MeetingResponse:
    meeting = await repository.update(meeting_id, **update.model_dump(exclude_none=True))
    return MeetingResponse.model_validate(meeting)


@router.get(
    path="/{meeting_id}",
    status_code=status.HTTP_200_OK,
    response_model=MeetingResponse,
    summary="Получение информации о встрече"
)
async def get_meeting(
        meeting_id: UUID, repository: MeetingRepository = Depends(get_meeting_repo)
) -> Meeting:
    meeting = await repository.read(meeting_id)
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MEETING_NOT_FOUND")
    return Meeting.model_validate(meeting)


@router.delete(
    path="/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление встречи",
)
async def delete_meeting(
        meeting_id: UUID, service: MeetingMediaService = Depends(get_meeting_media_service)
) -> None:
    return await service.delete(meeting_id)


@router.get(
    path="/{meeting_id}/transcript",
    status_code=status.HTTP_200_OK,
    response_model=Transcript,
    summary="Получение расшифровки встречи"
)
async def get_meeting_transcript(
        meeting_id: UUID, repository: TranscriptRepository = Depends(get_transcript_repo)
) -> Transcript:
    transcript = await repository.get_by_meeting(meeting_id)
    if transcript is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TRANSCRIPT_NOT_FOUND")
    return transcript


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[MeetingResponse],
)
async def get_meetings(repo: MeetingRepository = Depends(get_meeting_repo)) -> list[MeetingResponse]:
    ...
