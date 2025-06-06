from faststream import Logger
from faststream.rabbit import RabbitRouter

from dishka.integrations.base import FromDishka

from ...core.domain import Task, Meeting
from ...core.use_cases import ProtocolComposer
from ...core.base import FileRepository, TaskRepository


meetings_router = RabbitRouter()


@meetings_router.subscriber("tasks")
async def compose_protocol(
        task: Task,
        protocol_composer: FromDishka[ProtocolComposer],
        file_repository: FromDishka[FileRepository],
        task_repository: FromDishka[TaskRepository],
        logger: Logger
) -> None:
    logger.info("Start composing meeting protocol")
    audio_record = await file_repository.download_file(
        file_name=task.meeting_id,
        bucket_name="meetings"
    )
    meeting = Meeting(
        meeting_id=task.meeting_id,
        audio_record=audio_record,
        audio_format="mp3"
    )
    built_document = await protocol_composer.compose(meeting)
    logger.info("Finished composing meeting protocol")
    await file_repository.upload_file(
        file=built_document.file_buffer,
        file_name=built_document.document_id,
        bucket_name="protocols"
    )
    await task_repository.update(
        task_id=task.task_id,
        status="DONE",
        protocol_id=built_document.document_id
    )
    logger.info("Successfully saved meeting protocol")
