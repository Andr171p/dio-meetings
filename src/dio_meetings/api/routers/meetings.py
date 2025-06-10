from typing import Annotated

from uuid import UUID

from fastapi import APIRouter, status, HTTPException, UploadFile, File, Form
from fastapi.responses import Response

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ...core.services import MeetingService
from ...core.dto import MeetingUpload, CreatedMeeting


meetings_router = APIRouter(
    prefix="/api/v1/meetings", 
    tags=["Meetings"], 
    route_class=DishkaRoute
)


@meetings_router.post(
    path="/upload", 
    status_code=status.HTTP_201_CREATED,
    response_model=CreatedMeeting
)
async def upload_meeting(
        audio_file: Annotated[UploadFile, File(..., description="Аудио запись встречи/совещания")],
        name: Annotated[str, Form(..., description="Тема/название совещания")],
        speakers_count: Annotated[int, Form(..., description="Количество участников")],
        meeting_service: FromDishka[MeetingService]
) -> CreatedMeeting:
    file_data = await audio_file.read()
    meeting_upload = MeetingUpload(
        name=name,
        file_name=audio_file.filename,
        speakers_count=speakers_count,
        audio_bytes=file_data
    )
    created_meeting = await meeting_service.upload(meeting_upload)
    if not created_meeting:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while uploading meeting"
        )
    return created_meeting


@meetings_router.get(
    path="/{meeting_id}/download",
    status_code=status.HTTP_200_OK
)
async def download_meeting(
        meeting_id: UUID,
        meeting_service: FromDishka[MeetingService]
) -> Response:
    downloaded_meeting = await meeting_service.download(meeting_id)
    if not downloaded_meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    return Response(
        content=downloaded_meeting.file_data,
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"inline; filename={downloaded_meeting.file_name}"}
    )


@meetings_router.delete(
    path="/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_meeting(
        meeting_id: UUID,
        meeting_service: FromDishka[MeetingService]
) -> Response:
    is_deleted = await meeting_service.delete(meeting_id)
    if not is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
