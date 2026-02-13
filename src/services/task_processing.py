import logging
from pathlib import Path
from uuid import UUID

import aiofiles
import anyio

from .. import s3_utils
from ..ai_agent import generate_minutes
from ..database import repositories
from ..integrations import salute_speech
from ..schemas import Minutes, Transcript
from ..settings import TEMP_DIR
from ..utils.media import convert_video_to_audio, split_audio_into_chunks

TASKS_DIR = TEMP_DIR / "tasks"
TASKS_DIR.mkdir(exist_ok=True, parents=True)
CHUNK_SIZE = 8 * 1024 * 1024

logger = logging.getLogger(__name__)


class TaskProcessor:
    def __init__(
            self,
            meeting_repo: repositories.MeetingRepository,
            task_repo: repositories.TaskRepository,
            transcript_repo: repositories.TranscriptRepository,
            minutes_repo: repositories.MinutesRepository,
    ) -> None:
        self.meeting_repo = meeting_repo
        self.task_repo = task_repo
        self.transcript_repo = transcript_repo
        self.minutes_repo = minutes_repo

    async def prepare(self, meeting_id: UUID) -> Path:
        meeting = await self.meeting_repo.read(meeting_id)
        path = f"{TASKS_DIR}/{meeting.id}_{meeting.media_type}.{meeting.format}"
        file_path = anyio.Path(path)
        async with aiofiles.open(file_path, mode="wb") as file:
            async for chunk in s3_utils.download_multipart(
                    key=meeting.s3_key, chunk_size=CHUNK_SIZE
            ):
                await file.write(chunk)
            await file.flush()
        if meeting.media_type == "video":
            content = await convert_video_to_audio(file_path, output_format="mp3")
            path = f"{TASKS_DIR}/{meeting.id}_audio.mp3"
            file_path = anyio.Path(path)
            await file_path.write_bytes(content)
        return file_path

    async def transcribe(self, task_id: UUID, audio_file_path: Path) -> Transcript:
        chunks_dir = TASKS_DIR / "chunks"
        chunks_dir.mkdir(exist_ok=True)
        task = await self.task_repo.update(task_id, status="transcribing")
        texts = []
        for chunk in split_audio_into_chunks(
                audio_file_path, output_format="mp3", output_dir=chunks_dir
        ):
            content = await anyio.Path(chunk.file_path).read_bytes()
            text = await salute_speech.recognize_async(content, audio_encoding="MP3")
            texts.append(text)
        await anyio.Path(audio_file_path).unlink(missing_ok=True)
        full_text = "\n".join(texts)
        words_count = len(full_text.split(" "))
        transcript = Transcript(
            meeting_id=task.meeting_id, full_text=full_text, words_count=words_count
        )
        await self.transcript_repo.create(transcript)
        return transcript

    async def generate(self, task_id: UUID, full_text: str) -> None:
        task = await self.task_repo.update(task_id, status="generating")
        md_text = await generate_minutes(full_text)
        minutes = Minutes(meeting_id=task.meeting_id, title="Untitled", md_text=md_text)
        await self.minutes_repo.create(minutes)
        await self.task_repo.update(task_id, status="complete")

    async def process(self, task_id: UUID) -> None:
        task = await self.task_repo.update(task_id, status="processing")
        audio_file_path = await self.prepare(task.meeting_id)
        transcript = await self.transcribe(task_id, audio_file_path)
        await self.generate(task_id, transcript.full_text)
