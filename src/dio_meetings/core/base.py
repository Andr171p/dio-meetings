from typing import Optional, Protocol

from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from .domain import Meeting, Result
from .dto import (
    BaseMessage,
    AIMessage,
    Transcription,
    Document,
    TaskCreate,
    CreatedTask,
    CreatedMeeting,
    CreatedResult
)


class STTService(ABC):
    @abstractmethod
    async def transcript(
            self,
            audio_file: bytes,
            audio_format: str,
            speakers_count: int
    ) -> list[Transcription]: pass


class LLMService(ABC):
    @abstractmethod
    async def generate(self, messages: list[BaseMessage]) -> AIMessage: pass


class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self, text: str) -> Document: pass


class S3Repository(ABC):
    @abstractmethod
    async def upload_file(
            self,
            file_data: bytes,
            file_name: str,
            bucket_name: str
    ) -> None: pass

    @abstractmethod
    async def download_file(self, file_name: str, bucket_name: str) -> bytes: pass

    @abstractmethod
    async def delete_file(self, file_name: str, bucket_name: str) -> str: pass


class TaskRepository(ABC):
    @abstractmethod
    async def create(self, task: TaskCreate) -> CreatedTask: pass

    @abstractmethod
    async def read(self, task_id: UUID) -> Optional[CreatedTask]: pass

    @abstractmethod
    async def update(self, task_id: UUID, **kwargs) -> CreatedTask: pass

    @abstractmethod
    async def delete(self, task_id: UUID) -> bool: pass


class MeetingRepository(ABC):
    @abstractmethod
    async def create(self, meeting: Meeting) -> CreatedMeeting: pass

    @abstractmethod
    async def read(self, meeting_id: UUID) -> Optional[CreatedMeeting]: pass

    @abstractmethod
    async def read_all(self) -> list[CreatedMeeting]: pass

    # @abstractmethod
    # async def paginate(self, page: int, limit: int) -> list[CreatedMeeting]: pass

    @abstractmethod
    async def delete(self, meeting_id: UUID) -> bool: pass

    @abstractmethod
    async def get_result(self, meeting_id: UUID) -> Optional[CreatedResult]: pass


class ResultRepository(ABC):
    @abstractmethod
    async def create(self, result: Result) -> CreatedResult: pass

    @abstractmethod
    async def read(self, result_id: UUID) -> Optional[CreatedResult]: pass

    @abstractmethod
    async def delete(self, result_id: UUID) -> bool: pass


class BaseBroker(Protocol):
    async def publish(
            self,
            messages: BaseModel | list[BaseModel] | dict,
            **kwargs
    ) -> None: pass
