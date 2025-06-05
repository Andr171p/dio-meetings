from typing import Union

from abc import ABC, abstractmethod
from pathlib import Path
from uuid import UUID
import io

from .dto import BaseMessage, AIMessage, Transcription


class STTService(ABC):
    @abstractmethod
    async def transcript(self, file_path: Union[Path, str]) -> list[Transcription]: pass


class LLMService(ABC):
    @abstractmethod
    async def generate(self, messages: list[BaseMessage]) -> AIMessage: pass


class DocumentBuilder(ABC):
    @abstractmethod
    def build(self, text: str) -> UUID: pass


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
