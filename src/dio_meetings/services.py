from .base import BaseTranscripter


class MeetingProtocolService:
    def __init__(
            self,
            transcripter: BaseTranscripter
    ) -> None:
        self._transcripter = transcripter

    async def compose_protocol(self) -> ...:
        ...
