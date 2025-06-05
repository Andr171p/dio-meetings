from uuid import UUID

from .domain import Meeting
from .dto import SystemMessage, UserMessage, Transcription
from .base import STTService, LLMService, DocumentBuilder, FileRepository

from ..templates import PROTOCOL_TEMPLATE



class MeetingProtocolComposer:
    def __init__(
            self,
            stt_service: STTService,
            llm_service: LLMService,
            document_builder: DocumentBuilder,
            file_repository: FileRepository
    ) -> None:
        self._stt_service = stt_service
        self._llm_service = llm_service
        self._document_builder = document_builder
        self._file_repository = file_repository

    async def compose(self, meeting: Meeting) -> UUID:
        transcriptions = await self._stt_service.transcript(
            audio_file=meeting.audio_record,
            file_extension=meeting.audio_format
        )
        formated_transcriptions = self._format_transcriptions(transcriptions)
        messages = [SystemMessage(text=PROTOCOL_TEMPLATE), UserMessage(text=formated_transcriptions)]
        ai_message = await self._llm_service.generate(messages)
        built_document = self._document_builder.build(ai_message.text)
        await self._file_repository.upload_file(
            file=built_document.file_buffer,
            file_name=built_document.document_id,
            bucket_name="meetings-protocols"
        )
        return built_document.document_id

    @staticmethod
    def _format_transcriptions(transcriptions: list[Transcription]) -> str:
        return "\n\n".join([
            f"speaker_id: {transcription.speaker_id}, "
            f"text: {transcription.text}, "
            f"emotion: {transcription.emotion}"
            for transcription in transcriptions
        ])
