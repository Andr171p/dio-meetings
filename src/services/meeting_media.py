from typing import Literal

from uuid import UUID, uuid4

import aiofiles.tempfile
import anyio

from .. import s3_utils
from ..database.repositories import MeetingRepository
from ..schemas import Meeting
from ..settings import TEMP_DIR
from ..utils.media import BYTES_IN_MB, get_media_duration

MEDIA_DIR = TEMP_DIR / "media"
MEDIA_DIR.mkdir(exist_ok=True, parents=True)
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
        file_size_mb = round(len(content) / BYTES_IN_MB, 2)
        async with aiofiles.tempfile.NamedTemporaryFile(
            mode="wb", dir=MEDIA_DIR, suffix=f".{file_format}", delete=False
        ) as tmp_file:
            await tmp_file.write(content)
            await tmp_file.flush()
            tmp_file_path = anyio.Path(tmp_file.name)
        duration_seconds = get_media_duration(tmp_file_path)
        await tmp_file_path.unlink(missing_ok=True)
        meeting = Meeting(
            original_filename=filename,
            media_type=media_type,
            s3_key=s3_key,
            format=file_format,
            size_mb=file_size_mb,
            duration=duration_seconds,
        )
        await s3_utils.upload(content, key=s3_key)
        await self.repository.create(meeting)
        return meeting

    async def delete(self, meeting_id: UUID) -> None:
        meeting = await self.repository.read(meeting_id)
        await self.repository.delete(meeting_id)
        await s3_utils.delete(key=meeting.s3_key)
