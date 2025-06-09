from typing import Optional

from .domain import Meeting
from .dto import SystemMessage, UserMessage, Transcription, BuiltDocument
from .base import STTService, LLMService, DocumentBuilder

from ..templates import PROTOCOL_TEMPLATE


class ProtocolComposer:
    def __init__(
            self,
            stt_service: STTService,
            llm_service: LLMService,
            document_builder: DocumentBuilder
    ) -> None:
        self._stt_service = stt_service
        self._llm_service = llm_service
        self._document_builder = document_builder

    async def compose(self, meeting: Meeting) -> Optional[BuiltDocument]:
        transcriptions = await self._stt_service.transcript(
            audio_file=meeting.audio_record,
            file_extension=meeting.audio_format
        )
        formated_transcriptions = self._format_transcriptions(transcriptions)
        messages = [SystemMessage(text=PROTOCOL_TEMPLATE), UserMessage(text=formated_transcriptions)]
        ai_message = await self._llm_service.generate(messages)
        built_document = self._document_builder.build(ai_message.text)
        return built_document

    @staticmethod
    def _format_transcriptions(transcriptions: list[Transcription]) -> str:
        return "\n\n".join([
            f"speaker_id: {transcription.speaker_id}, "
            f"text: {transcription.text}, "
            f"emotion: {transcription.emotion}"
            for transcription in transcriptions
        ])
