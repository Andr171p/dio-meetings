from faststream import Logger
from faststream.rabbit import RabbitRouter

from dishka.integrations.base import FromDishka

from src.dio_meetings.core.domain import Meeting
from src.dio_meetings.core.base import FileRepository
from src.dio_meetings.core.use_cases import ProtocolComposer


meetings_router = RabbitRouter()


@meetings_router.subscriber("meetings")
async def compose_meeting_protocol(
        meeting: Meeting,
        meeting_protocol_composer: FromDishka[MeetingProtocolComposer],
        file_repository: FromDishka[FileRepository],
        logger: Logger
) -> None:
    logger.info("Start composing meeting protocol")
    built_document = await meeting_protocol_composer.compose(meeting)
    logger.info("Finished composing meeting protocol")
    await file_repository.upload_file(
        file=built_document.file_buffer,
        file_name=built_document.document_id,
        bucket_name="protocols"
    )
    logger.info("Successfully saved meeting protocol")
