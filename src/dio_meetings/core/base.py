from typing import Protocol, Optional, Union

from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from .dto import (
    BaseMessage,
    AIMessage,
    Transcription,
    BuiltDocument,
    TaskCreate,
    CreatedTask
)


class STTService(ABC):
    @abstractmethod
    async def transcript(
            self,
            audio_file: bytes,
            file_extension: str
    ) -> list[Transcription]: pass


class LLMService(ABC):
    @abstractmethod
    async def generate(self, messages: list[BaseMessage]) -> AIMessage: pass


class DocumentBuilder(ABC):
    @abstractmethod
    def build(self, text: str) -> BuiltDocument: pass


class FileRepository(ABC):
    @abstractmethod
    async def upload_file(
            self,
            file_data: bytes,
            file_name: str,
            bucket_name: str
    ) -> None: pass

    @abstractmethod
    async def download_file(self, file_name: str, bucket_name: str) -> ...: pass

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
