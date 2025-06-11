from typing import Optional

from uuid import UUID, uuid4
from datetime import datetime

from faststream.redis import RedisBroker

from .domain import Meeting, Result
from .dto import (
    Document,
    SystemMessage,
    UserMessage,
    CreatedTask,
    TaskCreate,
    MeetingUpload,
    CreatedMeeting,
    DownloadedFile,
    Transcription
)
from .base import (
    STTService,
    LLMService,
    DocumentFactory,
    S3Repository,
    TaskRepository,
    ResultRepository,
    MeetingRepository
)

from ..utils import get_file_format, get_audio_duration
from ..constants import MEETING_BUCKET_NAME, RESULT_BUCKET_NAME


class SummarizationService:
    def __init__(
            self,
            stt_service: STTService,
            llm_service: LLMService,
            document_factory: DocumentFactory
    ) -> None:
        self._stt_service = stt_service
        self._llm_service = llm_service
        self._document_factory = document_factory

    async def summarize(
            self,
            audio_file: bytes,
            audio_format: str,
            speakers_count: int,
            prompt_template: str
    ) -> Optional[Document]:
        '''
        transcriptions = await self._stt_service.transcript(
            audio_file=audio_file,
            audio_format=audio_format,
            speakers_count=speakers_count
        )
        formated_transcriptions = self._format_transcriptions(transcriptions)
        '''
        formated_transcriptions = "Здесь пока пусто это тест"
        messages = [SystemMessage(text=prompt_template), UserMessage(text=formated_transcriptions)]
        ai_message = await self._llm_service.generate(messages)
        document = self._document_factory.create_document(ai_message.text)
        print(document.file_data)
        return document

    @staticmethod
    def _format_transcriptions(transcriptions: list[Transcription]) -> str:
        return "\n\n".join([
            f"speaker_id: {transcription.speaker_id}, "
            f"text: {transcription.text}, "
            f"emotion: {transcription.emotion}"
            for transcription in transcriptions
        ])


class TaskService:
    def __init__(
            self,
            task_repository: TaskRepository,
            result_repository: ResultRepository,
            s3_repository: S3Repository,
            broker: RedisBroker
    ) -> None:
        self._task_repository = task_repository
        self._result_repository = result_repository
        self._s3_repository = s3_repository
        self._broker = broker

    async def create(self, meeting_id: UUID) -> Optional[CreatedTask]:
        task = TaskCreate(meeting_id=meeting_id, status="RUNNING")
        created_task = await self._task_repository.create(task)
        if not created_task:
            return None
        created_task.status = "NEW"
        await self._broker.publish(created_task, channel="tasks")
        return created_task

    async def update_status(self, task_id: UUID, document: Optional[Document]) -> None:
        if not document:
            await self._task_repository.update(
                task_id=task_id,
                status="ERROR"
            )
            return
        await self._s3_repository.upload_file(
            file_data=document.file_data,
            file_name=document.file_name,
            bucket_name=RESULT_BUCKET_NAME
        )
        await self._task_repository.update(
            task_id=task_id,
            status="DONE",
            result_id=document.id
        )
        result = Result(result_id=document.id, file_name=document.file_name)
        await self._result_repository.create(result)

    async def get_status(self, task_id: UUID) -> Optional[CreatedTask]:
        task = await self._task_repository.read(task_id)
        if not task:
            return None
        return task

    async def download_result(self, result_id: UUID) -> Optional[DownloadedFile]:
        result = await self._result_repository.read(result_id)
        if not result:
            return None
        file_data = await self._s3_repository.download_file(
            file_name=result.file_name,
            bucket_name=RESULT_BUCKET_NAME
        )
        print(file_data)
        print(75 * "=")
        print(result.file_name)
        return DownloadedFile(file_data=file_data, file_name=result.file_name)


class MeetingService:
    def __init__(
            self,
            meeting_repository: MeetingRepository,
            s3_repository: S3Repository
    ) -> None:
        self._meeting_repository = meeting_repository
        self._s3_repository = s3_repository

    async def upload(self, meeting_upload: MeetingUpload) -> CreatedMeeting:
        audio_format = get_file_format(meeting_upload.file_name)
        duration = get_audio_duration(meeting_upload.audio_bytes, audio_format)
        meeting_id = uuid4()
        file_name = f"{meeting_id}.{audio_format}"
        print(file_name)
        meeting = Meeting(
            meeting_id=meeting_id,
            name=meeting_upload.name,
            audio_format=audio_format,
            duration=duration,
            speakers_count=meeting_upload.speakers_count,
            file_name=file_name,
            date=datetime.now()
        )
        await self._s3_repository.upload_file(
            file_data=meeting_upload.audio_bytes,
            file_name=file_name,
            bucket_name=MEETING_BUCKET_NAME
        )
        created_meeting = await self._meeting_repository.create(meeting)
        return created_meeting

    async def download(self, meeting_id: UUID) -> Optional[DownloadedFile]:
        meeting = await self._meeting_repository.read(meeting_id)
        if not meeting:
            return None
        file_data = await self._s3_repository.download_file(
            file_name=meeting.file_name,
            bucket_name=MEETING_BUCKET_NAME
        )
        return DownloadedFile(file_data=file_data, file_name=meeting.file_name)

    async def delete(self, meeting_id: UUID) -> bool:
        meeting = await self._meeting_repository.read(meeting_id)
        if not meeting:
            return False
        is_deleted = await self._meeting_repository.delete(meeting_id)
        await self._s3_repository.delete_file(
            file_name=meeting.file_name,
            bucket_name=MEETING_BUCKET_NAME
        )
        return is_deleted
