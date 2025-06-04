from uuid import UUID

from fastapi import APIRouter, status, UploadFile

from ..schemas import AcceptedMeeting


meetings_router = APIRouter(
    prefix="/api/v1/meetings",
    tags=["Meetings"],
)


@meetings_router.post(
    path="/upload-file",
    status_code=status.HTTP_201_CREATED,
    response_model=AcceptedMeeting
)
async def upload_meeting(file: UploadFile) -> AcceptedMeeting:
    ...


@meetings_router.get(
    path="/{meeting_id}",
    status_code=status.HTTP_200_OK,
    response_model=...
)
async def get_meeting(meeting_id: UUID) -> ...:
    ...
