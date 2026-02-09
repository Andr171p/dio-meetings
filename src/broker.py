from uuid import UUID

from faststream import Logger
from faststream.redis import RedisBroker
from pydantic import BaseModel

from . import s3_storage
from .database import repositories
from .database.base import session_factory
from .integrations import salute_speech
from .schemas import Minutes
from .settings import settings
from .utils import generate_meeting_minutes, split_audio_into_chunks

broker = RedisBroker(settings.redis.url)


@broker.subscriber("minutes:create")
async def process_task(task_id: UUID, logger: Logger) -> None:
    file = await s3_storage.download(message.s3_key)
    logger.info(
        "Downloaded file %s mb by key %s", round(len(file) / 1_000_000, 2), message.s3_key
    )
    async with session_factory() as session:
        transcribed_chunks = []
        for chunk in split_audio_into_chunks(
                file, audio_format=message.audio_format, output_format="mp3"
        ):
            chunk_transcript = await salute_speech.recognize_async(
                audio_file=chunk.content, audio_encoding="MP3"
            )
            transcribed_chunks.append(chunk_transcript)
        full_transcript = "\n".join(transcribed_chunks)
        logger.info(
            "Start generate minutes of meeting, transcript %s characters", len(full_transcript)
        )
        md_text = await generate_meeting_minutes(full_transcript)
        summary = md_text.replace("```", "").replace("markdown", "")
        await repository.add_meeting_minutes(
            session, MeetingMinutes(
                task_id=message.task_id,
                transcript=full_transcript,
                summary=summary,
                audio_s3_key=message.s3_key,
            )
        )
        await repository.update_task_status(
            session, task_id=message.task_id, status="complete"
        )
        await session.commit()
        logger.info("Minutes of meeting generation completed!")
