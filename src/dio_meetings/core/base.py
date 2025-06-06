from typing import Protocol, Optional, Union

from abc import ABC, abstractmethod
from uuid import UUID
import io

from pydantic import BaseModel

from domain import Task
from .dto import BaseMessage, AIMessage, Transcription, BuiltDocument, TaskCreate, TaskRead


class STTService(ABC):
    @abstractmethod
    async def transcript(
            self,
            audio_file: Union[io.BytesIO, bytes],
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
            file: Union[io.BytesIO, bytes],
            file_name: Union[UUID, str],
            bucket_name: str
    ) -> None: pass

    @abstractmethod
    async def download_file(self, file_name: Union[UUID, str], bucket_name: str) -> ...: pass

    @abstractmethod
    async def delete_file(self, file_name: Union[UUID, str], bucket_name: str) -> str: pass


class MessageBroker(Protocol):
    async def publish(
            self,
            messages: Union[BaseModel, list[BaseModel], dict],
            queue: str
    ) -> None: pass


class TaskRepository(ABC):
    @abstractmethod
    async def create(self, task: TaskCreate) -> TaskRead: pass

    @abstractmethod
    async def read(self, task_id: UUID) -> Optional[TaskRead]: pass

    @abstractmethod
    async def update(self, task: Task) -> TaskRead: pass

    @abstractmethod
    async def delete(self, task_id: UUID) -> bool: pass
