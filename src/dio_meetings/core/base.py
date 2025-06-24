from typing import Optional, Protocol

from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from .domain import FileMetadata, File, Task
from .dto import BaseMessage, AIMessage, Transcription


class BaseSTT(ABC):
    @abstractmethod
    async def transcribe(
            self,
            audio_data: bytes,
            audio_format: str,
            speakers_count: int
    ) -> list[Transcription]: pass


class BaseLLM(ABC):
    @abstractmethod
    async def generate(self, messages: list[BaseMessage]) -> AIMessage: pass


class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self, text: str) -> File: pass


class FileStorage(ABC):
    @abstractmethod
    async def upload_file(self, data: bytes, key: str, bucket: str) -> None: pass

    @abstractmethod
    async def download_file(self, key: str, bucket: str) -> bytes: pass

    @abstractmethod
    async def remove_file(self, key: str, bucket: str) -> str: pass


class FileMetadataRepository(ABC):
    @abstractmethod
    async def create(self, file_metadata: FileMetadata) -> FileMetadata: pass

    @abstractmethod
    async def read(self, id: UUID) -> Optional[FileMetadata]: pass

    @abstractmethod
    async def read_all(self, bucket: Optional[str] = None) -> list[FileMetadata]: pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool: pass


class TaskRepository(ABC):
    @abstractmethod
    async def create(self, task: Task) -> Task: pass

    @abstractmethod
    async def read(self, id: UUID) -> Optional[Task]: pass

    @abstractmethod
    async def update(self, id: UUID, **kwargs) -> Task: pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool: pass


class BaseBroker(Protocol):
    async def publish(
            self,
            messages: BaseModel | list[BaseModel] | dict,
            **kwargs
    ) -> None: pass
