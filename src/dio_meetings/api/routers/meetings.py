from uuid import UUID

from fastapi import APIRouter, status

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ..params import AudioFile, AcceptedMeeting

from src.dio_meetings.core.base import FileRepository


meetings_router = APIRouter(
    prefix="/api/v1/meetings", 
    tags=["Meetings"], 
    route_class=DishkaRoute
)


@meetings_router.post(
    path="/upload", 
    status_code=status.HTTP_202_ACCEPTED, 
    response_model=AcceptedMeeting
)
async def upload_meeting(
        audio_file: AudioFile,
        file_repository: FromDishka[FileRepository]
) -> ...:
    content = await audio_file.read()
    await file_repository.upload_file(
        file=content,
        file_name=audio_file.filename,
        bucket_name="meetings"
    )
    return ...
