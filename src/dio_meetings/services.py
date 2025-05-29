

class MeetingTranscriptor:
    def __init__(self) -> None:
        ...

    async def transcript(self) -> str:
        ...


class ProtocolWriter:
    def __init__(self) -> None:
        ...

    async def write(self) -> str:
        ...
