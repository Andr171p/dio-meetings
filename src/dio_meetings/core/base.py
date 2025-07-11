from typing import Optional, Protocol, Generic, TypeVar, Union

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .enums import FileType
from .domain import FileMetadata, File
from .dto import BaseMessage, AIMessage, Transcription

T = TypeVar("T", bound=BaseModel)

Id = Union[int, str, UUID]


class CRUDRepository(Generic[T]):
    async def create(self, model: T) -> T: pass

    async def read(self, id: Id) -> Optional[T]: pass

    async def update(self, id: Id, **kwargs) -> Optional[T]: pass

    async def delete(self, id: Id) -> bool: pass


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


class FileMetadataRepository(CRUDRepository[FileMetadata]):
    async def read_all(
            self,
            page: int,
            limit: int,
            bucket: Optional[str] = None
    ) -> list[FileMetadata]: pass

    async def filter_by_date_range(
            self,
            start_date: datetime,
            end_date: datetime,
            type: Optional[FileType] = None,
    ) -> list[FileMetadata]: pass

    async def get_today(self, type: Optional[FileType] = None) -> list[FileMetadata]: pass

    async def get_result(self, id: UUID) -> Optional[FileMetadata]: pass

    async def count(self, type: Optional[FileType] = None) -> int: pass


class BaseBroker(Protocol):
    async def publish(self, messages: BaseModel | list[BaseModel] | dict, **kwargs) -> None: pass
