from uuid import uuid4

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import StreamingResponse

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ..params import AudioFile

from ...core.base import FileRepository
from ...core.dto import UploadedMeeting
from ...utils import get_file_extension
from ...constants import MEETINGS_BUCKET_NAME


meetings_router = APIRouter(
    prefix="/api/v1/meetings", 
    tags=["Meetings"], 
    route_class=DishkaRoute
)


@meetings_router.post(
    path="/upload", 
    status_code=status.HTTP_201_CREATED,
    response_model=UploadedMeeting
)
async def upload_meeting(
        audio_file: AudioFile,
        file_repository: FromDishka[FileRepository]
) -> UploadedMeeting:
    content = await audio_file.read()
    meeting_id = uuid4()
    file_format = get_file_extension(audio_file.filename)
    meeting_key = f"{meeting_id}.{file_format}"
    await file_repository.upload_file(
        file=content,
        file_name=meeting_key,
        bucket_name=MEETINGS_BUCKET_NAME
    )
    return UploadedMeeting(meeting_key=meeting_key)


@meetings_router.get(
    path="/{meeting_key}/download",
    status_code=status.HTTP_200_OK
)
async def download_meeting(
        meeting_key: str,
        file_repository: FromDishka[FileRepository]
) -> StreamingResponse:
    file_data = await file_repository.download_file(
        file_name=meeting_key,
        bucket_name=MEETINGS_BUCKET_NAME
    )
    if not file_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    return StreamingResponse(
        content=file_data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={meeting_key}"}
    )


@meetings_router.delete(
    path="/{meeting_key}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_meeting(
        meeting_key: str,
        file_repository: FromDishka[FileRepository]
) -> None:
    await file_repository.delete_file(
        file_name=meeting_key,
        bucket_name=MEETINGS_BUCKET_NAME
    )
