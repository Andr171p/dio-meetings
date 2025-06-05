from faststream import Logger
from faststream.rabbit import RabbitRouter

from dishka.integrations.base import FromDishka

from src.dio_meetings.core.domain import Meeting
from src.dio_meetings.core.use_cases import MeetingProtocolComposer


meetings_router = RabbitRouter()


@meetings_router.subscriber("meetings")
async def compose_meeting_protocol(
        meeting: Meeting,
        meeting_protocol_composer: FromDishka[MeetingProtocolComposer],
        logger: Logger
) -> ...:
    logger.info("Start composing meeting protocol")
    protocol_id = await meeting_protocol_composer.compose(meeting)
    logger.info("Finished composing meeting protocol")
