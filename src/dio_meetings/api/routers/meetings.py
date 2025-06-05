from uuid import UUID

from fastapi import APIRouter, status

from faststream.rabbit import RabbitBroker

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ..schemas import (
    AudioFile,
    TitleForm,
    ParticipantsForm,
    AcceptedMeeting,
    MeetingStatus
)


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
        title: TitleForm,
        participants: ParticipantsForm,
        broker: FromDishka[RabbitBroker]
) -> AcceptedMeeting:
    ...


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
