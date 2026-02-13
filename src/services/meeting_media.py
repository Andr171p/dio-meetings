from typing import Literal

import logging
from collections.abc import AsyncIterable
from pathlib import Path
from uuid import UUID, uuid4

import aiofiles
import anyio
from fastapi import UploadFile

from .. import s3_utils
from ..database.repositories import MeetingRepository
from ..schemas import Meeting
from ..settings import TEMP_DIR
from ..utils.media import get_media_duration

MEDIA_DIR = TEMP_DIR / "media"
MEDIA_DIR.mkdir(exist_ok=True, parents=True)
AUDIO_FORMATS = {"mp3", "wav", "m4a", "flac", "aac", "ogg", "oga"}
VIDEO_FORMATS = {"mp4", "webm"}
CHUNK_SIZE = 8 * 1024 * 1024  # Размер чанка для загрузки файла в память

logger = logging.getLogger(__name__)


async def generate_chunks(file_path: Path) -> AsyncIterable[bytes]:
    async with aiofiles.open(file_path, mode="rb") as file:
        while chunk := await file.read(CHUNK_SIZE):
            yield chunk


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

    async def upload_and_create(self, file: UploadFile) -> Meeting:
        try:
            logger.info(
                "Start uploading and creating file `%s` with size %s mb ...",
                file.filename, round(file.size / 1024 * 1024, 2)
            )
            suffix = Path(file.filename).suffix
            async with aiofiles.tempfile.NamedTemporaryFile(
                mode="wb", dir=MEDIA_DIR, suffix=suffix, delete=False
            ) as tmp_file:
                while chunk := await file.read(CHUNK_SIZE):
                    await tmp_file.write(chunk)
                await tmp_file.flush()
                tmp_file_path = anyio.Path(tmp_file.name)
                logger.info("File persisted for ")
            file_stat = await tmp_file_path.stat()
            s3_key = f"{uuid4()}{suffix}"
            duration_seconds = get_media_duration(tmp_file_path)
            meeting = Meeting(
                original_filename=file.filename,
                media_type=define_media_type(file.filename),
                s3_key=s3_key,
                format=suffix[1:],
                size_mb=round(file_stat.st_size / 1024 * 1024, 2),
                duration=duration_seconds,
            )
            chunks = generate_chunks(tmp_file_path)
            await s3_utils.upload_multipart(chunks, key=s3_key)
            await self.repository.create(meeting)
            return meeting
        finally:
            await tmp_file_path.unlink(missing_ok=True)

    async def delete(self, meeting_id: UUID) -> None:
        meeting = await self.repository.read(meeting_id)
        await self.repository.delete(meeting_id)
        await s3_utils.delete(key=meeting.s3_key)
