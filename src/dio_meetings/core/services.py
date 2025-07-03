from typing import Optional

from uuid import UUID, uuid4
from datetime import datetime

from .enums import FileType, TaskStatus
from .domain import File, FileMetadata, Task
from .dto import SystemMessage, UserMessage, Transcription
from .base import (
    BaseSTT,
    BaseLLM,
    BaseBroker,
    DocumentFactory,
    FileStorage,
    CRUDRepository,
    FileMetadataRepository
)
from .exceptions import (
    UpdatingError,
    CreationError,
    UploadingError,
    TaskCreationError,
    TaskStatusUpdatingError
)

from ..utils import generate_file_name, get_document_file_name
from ..constants import DOCUMENTS_BUCKET


class SummarizationService:
    def __init__(self, stt: BaseSTT, llm: BaseLLM, document_factory: DocumentFactory) -> None:
        self._stt = stt
        self._llm = llm
        self._document_factory = document_factory

    async def summarize(self, audio: File, speakers_count: int, prompt_template: str) -> Optional[File]:
        if audio.type != FileType.AUDIO:
            raise ValueError("File type must be audio")
        transcriptions = await self._stt.transcribe(
            audio_data=audio.data,
            audio_format=audio.format,
            speakers_count=speakers_count
        )
        formated_transcriptions = self._format_transcriptions(transcriptions)
        messages = [SystemMessage(text=prompt_template), UserMessage(text=formated_transcriptions)]
        ai_message = await self._llm.generate(messages)
        document = self._document_factory.create_document(ai_message.text)
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
            task_repository: CRUDRepository[Task],
            file_metadata_repository: FileMetadataRepository,
            file_storage: FileStorage,
            broker: BaseBroker
    ) -> None:
        self._task_repository = task_repository
        self._file_metadata_repository = file_metadata_repository
        self._file_storage = file_storage
        self._broker = broker

    async def create(self, file_id: UUID) -> Optional[Task]:
        try:
            task = Task(file_id=file_id, status=TaskStatus.RUNNING)
            created_task = await self._task_repository.create(task)
            created_task.status = TaskStatus.NEW
            await self._broker.publish(created_task, channel="tasks")
            return created_task
        except CreationError as e:
            raise TaskCreationError(f"Error while task creation: {e}") from e

    async def update_status(self, task_id: UUID, document: Optional[File]) -> None:
        if document.type != FileType.DOCUMENT and document:
            raise ValueError("File type must be document")
        try:
            if not document:
                await self._task_repository.update(id=task_id, status=TaskStatus.ERROR)
                return
            key = generate_file_name(document.format)
            result_id = uuid4()
            await self._file_storage.upload_file(data=document.data, key=key, bucket=DOCUMENTS_BUCKET)
            await self._task_repository.update(id=task_id, status=TaskStatus.DONE, result_id=result_id)
            file_metadata = FileMetadata(
                id=result_id,
                file_name=get_document_file_name(document.format),
                key=key,
                bucket=DOCUMENTS_BUCKET,
                size=document.size,
                format=document.format,
                type=document.type,
                uploaded_date=datetime.now()
            )
            await self._file_metadata_repository.create(file_metadata)
        except (UpdatingError, UploadingError, CreationError) as e:
            raise TaskStatusUpdatingError(f"Error while updating task status: {e}") from e

    async def get_status(self, task_id: UUID) -> Optional[Task]:
        task = await self._task_repository.read(task_id)
        if not task:
            return None
        return task


class FileService:
    def __init__(
            self,
            file_metadata_repository: FileMetadataRepository,
            file_storage: FileStorage
    ) -> None:
        self._file_metadata_repository = file_metadata_repository
        self._file_storage = file_storage

    async def upload(self, file: File, bucket: str) -> FileMetadata:
        key = generate_file_name(file.format)
        await self._file_storage.upload_file(data=file.data, key=key, bucket=bucket)
        file_metadata = FileMetadata(
            file_name=file.file_name,
            key=key,
            bucket=bucket,
            size=file.size,
            format=file.format,
            type=file.type,
            uploaded_date=datetime.now()
        )
        created_file_metadata = await self._file_metadata_repository.create(file_metadata)
        return created_file_metadata

    async def download(self, id: UUID, bucket: str) -> Optional[File]:
        file_metadata = await self._file_metadata_repository.read(id)
        if not file_metadata:
            return None
        data = await self._file_storage.download_file(key=file_metadata.key, bucket=bucket)
        return File(data=data, file_name=file_metadata.key)

    async def remove(self, id: UUID, bucket: str) -> bool:
        file_metadata = await self._file_metadata_repository.read(id)
        if not file_metadata:
            return False
        is_deleted = await self._file_metadata_repository.delete(id)
        await self._file_storage.remove_file(key=file_metadata.key, bucket=bucket)
        return is_deleted
