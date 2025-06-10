from faststream import Logger
from faststream.redis import RedisRouter

from dishka.integrations.base import FromDishka

from ...core.domain import Task
from ...utils import get_file_format
from ...constants import SPEAKERS_COUNT
from ...templates import SUMMARY_TEMPLATE
from ...core.services import TaskService, SummarizationService, MeetingService


meetings_router = RedisRouter()


@meetings_router.subscriber("tasks")
async def summarize_meeting(
        task: Task,
        meeting_service: FromDishka[MeetingService],
        summarization_service: FromDishka[SummarizationService],
        task_service: FromDishka[TaskService],
        logger: Logger
) -> None:
    logger.info("Start summarize meeting")
    downloaded_file = await meeting_service.download(task.meeting_id)
    document = await summarization_service.summarize(
        audio_file=downloaded_file.file_data,
        audio_format=get_file_format(downloaded_file.file_name),
        speakers_count=SPEAKERS_COUNT,
        prompt_template=SUMMARY_TEMPLATE
    )
    logger.info("Finished summarizing meeting")
    await task_service.update_status(task_id=task.task_id, document=document)
