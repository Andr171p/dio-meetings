from typing import Literal

from uuid import UUID, uuid4

from tinytag import TinyTag

from .. import s3_utils
from ..database.repositories import MeetingRepository
from ..schemas import Meeting
from ..utils.audio import BYTES_IN_MB

AUDIO_FORMATS = {"mp3", "wav", "m4a", "flac", "aac", "ogg", "oga"}
VIDEO_FORMATS = {"mp4", "webm"}


def define_media_type(filename: str) -> Literal["audio", "video"]:
    file_format = filename.rsplit(".", maxsplit=1)[-1]
    if file_format in AUDIO_FORMATS:
        return "audio"
    if file_format in VIDEO_FORMATS:
        return "video"
    raise ValueError(f"Unsupported file format: {file_format}!")


class MeetingMediaService:
    def __init__(self, repository: MeetingRepository) -> None:
        self.repository = repository

    async def upload_and_create(self, content: bytes, filename: str) -> Meeting:
        file_format = filename.rsplit(".", maxsplit=1)[-1]
        s3_key = f"{uuid4()}.{file_format}"
        media_type = define_media_type(filename)
        tag = TinyTag.get(content)
        file_size_mb = round(len(content) / BYTES_IN_MB, 2)
        meeting = Meeting(
            original_filename=filename,
            media_type=media_type,
            s3_key=s3_key,
            format=file_format,
            size_mb=file_size_mb,
            duration=tag.duration,
        )
        await s3_utils.upload(content, key=s3_key)
        await self.repository.create(meeting)
        return meeting

    async def delete(self, meeting_id: UUID) -> None:
        meeting = await self.repository.read(meeting_id)
        await self.repository.delete(meeting_id)
        await s3_utils.delete(key=meeting.s3_key)
