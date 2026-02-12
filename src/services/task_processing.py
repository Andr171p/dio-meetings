import logging
import time
from uuid import UUID

from .. import s3_utils
from ..ai_agent import generate_minutes
from ..database import repositories
from ..integrations import salute_speech
from ..schemas import Minutes, Transcript
from ..utils import split_audio_into_chunks, video_to_audio

logger = logging.getLogger(__name__)


class TaskHandler:
    def __init__(
            self,
            meeting_repo: repositories.MeetingRepository,
            task_repo: repositories.TaskRepository,
            transcript_repo: repositories.TranscriptRepository,
            minutes_repo: repositories.MinutesRepository
    ) -> None:
        self.meeting_repo = meeting_repo
        self.task_repo = task_repo
        self.transcript_repo = transcript_repo
        self.minutes_repo = minutes_repo

    async def handle(self, task_id: UUID) -> None:  # noqa: PLR0914
        start_time = time.monotonic()
        task = await self.task_repo.read(task_id)
        meeting = await self.meeting_repo.read(task.meeting_id)
        file_format = meeting.format
        logger.info("Starting meeting downloading ...")
        await self.task_repo.update(task.id, status="processing")
        download_start = time.monotonic()
        file = await s3_utils.download(meeting.s3_key)
        logger.info(
            "File downloaded from S3, time elapsed %s seconds", time.monotonic() - download_start
        )
        if meeting.media_type == "video":
            logger.info("Starting convertion video to audio")
            conv_start = time.monotonic()
            file = video_to_audio(file, video_format=file_format, output_format="mp3")
            file_format = "mp3"
            logger.info(
                "Video converted to audio, time elapsed %s seconds", time.monotonic() - conv_start
            )
        texts = []
        await self.task_repo.update(task.id, status="transcribing")
        logger.info("Starting audio transcription ...")
        transcribe_start = time.monotonic()
        for i, chunk in enumerate(split_audio_into_chunks(
                file, audio_format=file_format, output_format="mp3"
        )):
            text = await salute_speech.recognize_async(chunk.content, audio_encoding="MP3")
            logger.info(
                "Transcribes %s chunk, time elapsed %s seconds",
                i + 1, time.monotonic() - transcribe_start
            )
            texts.append(text)
        full_text = "\n".join(texts)
        words_count = len(full_text.split(" "))
        transcript = Transcript(
            meeting_id=meeting.id, full_text=full_text, words_count=words_count
        )
        await self.transcript_repo.create(transcript)
        await self.task_repo.update(task.id, status="generating")
        logger.info("Starting generating minutes of meeting ...")
        md_text = await generate_minutes(full_text)
        md_text = md_text.replace("```", "").replace("markdown", "")
        title = meeting.original_filename.replace("", meeting.format)
        minutes = Minutes(meeting_id=meeting.id, title=title, md_text=md_text)
        await self.minutes_repo.create(minutes)
        await self.task_repo.update(task.id, status="complete")
        logger.info("Task completed, time elapsed %s seconds", time.monotonic() - start_time)
