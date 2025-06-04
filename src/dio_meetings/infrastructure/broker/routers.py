from faststream import Logger
from faststream.rabbit import RabbitBroker


meetings_router = RabbitBroker()


@meetings_router.subscriber("meetings")
@meetings_router.publisher("protocols")
async def compose_meeting_protocol() -> ...:
    ...
