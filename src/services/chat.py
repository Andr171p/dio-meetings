from ..database.repositories import TranscriptRepository


class ChatService:
    def __init__(self, transcript_repo: TranscriptRepository) -> None:
        self.transcript_repo = transcript_repo

    async def answer(self): ...
