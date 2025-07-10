from typing import Optional

from faststream import Logger
from faststream.redis import RedisRouter

from dishka.integrations.base import FromDishka as Depends

from ...core.domain import Task, File
from ...core.services import FileService, SummarizationService, TaskService
from ...core.exceptions import SummarizationError

from ...constants import SPEAKERS_COUNT, AUDIO_BUCKET
from ...templates import SUMMARY_TEMPLATE

tasks_router = RedisRouter()


@tasks_router.subscriber("tasks")
async def summarize_audio(
        task: Task,
        file_service: Depends[FileService],
        summarization_service: Depends[SummarizationService],
        task_service: Depends[TaskService],
        logger: Logger
) -> None:
    logger.info("Start summarize audio")
    downloaded_file = await file_service.download(task.file_id, bucket=AUDIO_BUCKET)
    document: Optional[File] = None
    try:
        document = await summarization_service.summarize(
            audio=downloaded_file,
            speakers_count=SPEAKERS_COUNT,
            prompt_template=SUMMARY_TEMPLATE
        )
    except SummarizationError:
        logger.error("Error while summarize audio")
    await task_service.update_status(task_id=task.id, document=document)
    logger.info("Finished summarizing audio")
