from uuid import UUID, uuid4

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import StreamingResponse

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ..params import AudioFile

from ...core.base import FileRepository
from ...core.dto import UploadingMeeting


meetings_router = APIRouter(
    prefix="/api/v1/meetings", 
    tags=["Meetings"], 
    route_class=DishkaRoute
)


@meetings_router.post(
    path="/upload", 
    status_code=status.HTTP_202_ACCEPTED, 
    response_model=UploadingMeeting
)
async def upload_meeting(
        audio_file: AudioFile,
        file_repository: FromDishka[FileRepository]
) -> UploadingMeeting:
    content = await audio_file.read()
    meeting_id = uuid4()
    await file_repository.upload_file(
        file=content,
        file_name=meeting_id,
        bucket_name="meetings"
    )
    return UploadingMeeting(meeting_id=meeting_id)


@meetings_router.get(
    path="/{meeting_id}/download",
    status_code=status.HTTP_200_OK
)
async def download_meeting(
        meeting_id: UUID,
        file_repository: FromDishka[FileRepository]
) -> StreamingResponse:
    file_content = await file_repository.download_file(
        file_name=meeting_id,
        bucket_name="meetings"
    )
    if not file_content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    return StreamingResponse(
        content=file_content,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={meeting_id}"}
    )


@meetings_router.delete(
    path="/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_meeting(
        meeting_id: UUID,
        file_repository: FromDishka[FileRepository]
) -> None:
    await file_repository.delete_file(
        file_name=meeting_id,
        bucket_name="meetings"
    )
