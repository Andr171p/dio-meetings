from uuid import uuid4

from .. import s3_storage
from ..broker import GenerationMessage, broker
from ..database import repository
from ..database.base import session_factory
from ..schemas import Task


async def create_task(file: bytes, filename: str) -> Task:
    audio_format = filename.rsplit(".", maxsplit=1)[-1]
    s3_key = f"{uuid4()}.{audio_format}"
    async with session_factory() as session:
        task = Task(
            filename=filename, audio_s3_key=s3_key, status="processing"
        )
        await repository.add_task(session, task)
        await s3_storage.upload(file, key=s3_key)
        await broker.publish(
            GenerationMessage(
                task_id=task.id, audio_format=audio_format, s3_key=s3_key
            ), channel="meeting-minutes:generate"
        )
        await session.commit()
    return task
