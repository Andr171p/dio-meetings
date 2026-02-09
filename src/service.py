from typing import Literal

from uuid import UUID, uuid4

from . import s3_storage, schemas
from .broker import broker
from .database.base import session_factory
from .database.repositories import MeetingRepository, TaskRepository
from .utils import AudioChunk, get_audio_duration, get_video_duration

AUDIO_FORMATS = {"mp3", "wav", "m4a", "flac", "aac", "ogg", "oga"}
VIDEO_FORMATS = {"mp4", "webm"}


def define_content_type(filename: str) -> Literal["audio", "video"]:
    suffix = filename.rsplit(".", maxsplit=1)[-1]
    if suffix in AUDIO_FORMATS:
        return "audio"
    if suffix in VIDEO_FORMATS:
        return "video"
    raise ValueError(f"Unsupported file type: {suffix}")


async def upload_meeting(file: bytes, filename: str) -> schemas.Meeting:
    suffix = filename.rsplit(".", maxsplit=1)[-1]
    s3_key = f"{uuid4()}.{suffix}"
    async with session_factory() as session:
        await s3_storage.upload(file, key=s3_key)
        content_type = define_content_type(filename)
        if content_type == "audio":
            duration = get_audio_duration(file)
        else:
            duration = get_video_duration(file, video_format=suffix)
        size_mb = round(len(file) / 1_000_000, 2)
        meeting = schemas.Meeting(
            original_filename=filename,
            content_type=content_type,
            s3_key=s3_key,
            format=suffix,
            size_mb=size_mb,
            duration=duration,
        )
        repository = MeetingRepository(session)
        await repository.create(meeting)
        await session.commit()
    return meeting


async def delete_meeting(meeting_id: UUID) -> None:
    async with session_factory() as session:
        repository = MeetingRepository(session)
        meeting = await repository.read(meeting_id)
        await repository.delete(meeting_id)
        await s3_storage.delete(meeting.s3_key)
        await session.commit()


async def create_task(meeting_id: UUID) -> schemas.Task:
    async with session_factory() as session:
        repository = TaskRepository(session)
        task = schemas.Task(meeting_id=meeting_id, status="pending")
        await repository.create(task)
        await session.commit()
        await broker.publish(task.id, channel="minutes:create")
    return task


async def process_meeting(meeting_id: UUID) -> ...:
    ...
