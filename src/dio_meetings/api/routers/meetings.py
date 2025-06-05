from uuid import UUID

from fastapi import APIRouter, status, BackgroundTasks

from faststream.rabbit import RabbitBroker

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ..schemas import AudioFile, AcceptedMeeting, MeetingStatus

from src.dio_meetings.core.domain import Meeting
from src.dio_meetings.utils import get_file_extension


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
        broker: FromDishka[RabbitBroker],
        background_tasks: BackgroundTasks
) -> AcceptedMeeting:
    data = await audio_file.read()
    file_extension = get_file_extension(audio_file.filename)
    meeting = Meeting(audio_record=data, audio_format=file_extension)
    background_tasks.add_task(
        broker.publish,
        meeting,
        queue="meetings"
    )
    return AcceptedMeeting(meeting_id=meeting.meeting_id)


@meetings_router.get(
    path="/{meeting_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=MeetingStatus,
)
async def get_meeting_status(meeting_id: UUID) -> MeetingStatus: ...


@meetings_router.get(
    path="/{meeting_id}", 
    status_code=status.HTTP_200_OK, 
    response_model=...
)
async def get_meeting(meeting_id: UUID) -> ...: ...
