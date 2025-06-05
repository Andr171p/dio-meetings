from typing import Union

from abc import ABC, abstractmethod
from pathlib import Path

from .dto import BaseMessage, AIMessage, Transcription


class STTService(ABC):
    @abstractmethod
    async def transcript(self, file_path: Union[Path, str]) -> list[Transcription]: pass


class LLMService(ABC):
    @abstractmethod
    async def generate(self, messages: list[BaseMessage]) -> AIMessage: pass
