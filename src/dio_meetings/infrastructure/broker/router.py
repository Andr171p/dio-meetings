from faststream import Logger
from faststream.redis import RedisRouter

from dishka.integrations.base import FromDishka

from ...core.domain import Task
from ...constants import SPEAKERS_COUNT
from ...templates import SUMMARY_TEMPLATE
from ...core.services import TaskService, SummarizationService, FileService


tasks_router = RedisRouter()


@tasks_router.subscriber("tasks")
async def summarize_audio(
        task: Task,
        file_service: FromDishka[FileService],
        summarization_service: FromDishka[SummarizationService],
        task_service: FromDishka[TaskService],
        logger: Logger
) -> None:
    logger.info("Start summarize meeting")
    downloaded_file = await file_service.download(task.file_id, bucket="audio")
    document = await summarization_service.summarize(
        audio=downloaded_file,
        speakers_count=SPEAKERS_COUNT,
        prompt_template=SUMMARY_TEMPLATE
    )
    await task_service.update_status(task_id=task.task_id, document=document)
    logger.info("Finished summarizing meeting")
