import asyncio
import logging

from src.dio_meetings.ioc import container
from src.dio_meetings.core.use_cases import MeetingProtocolComposer


file_path = "Ivashko Alexadr G(0079222696701)_20250527131818.mp3"


async def main() -> None:
    meeting_protocol_composer: MeetingProtocolComposer = await container.get(MeetingProtocolComposer)
    protocol = await meeting_protocol_composer.compose(file_path)
    print(protocol)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
