import asyncio
import logging

from src.dio_meetings.ioc import container
from src.dio_meetings.core.use_cases import MeetingProtocolComposer


file_path = "847y7aiqteg40hi6gu7ok7t7lrolqprb.mp3"


async def main() -> None:
    meeting_protocol_composer: MeetingProtocolComposer = await container.get(MeetingProtocolComposer)
    protocol = await meeting_protocol_composer.compose(file_path)
    print(protocol)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
