from typing import Union

from abc import ABC, abstractmethod
from pathlib import Path

from src.dio_meetings.core.entities import BaseMessage, Transcription
from src.dio_meetings.infrastructure.ai.yandex_gpt.schemas import AssistantMessage


class BaseTranscripter(ABC):
    @abstractmethod
    async def transcript(self, file_path: Union[Path, str]) -> list[Transcription]: pass


class BaseLLM(ABC):
    @abstractmethod
    async def generate(self, messages: list[BaseMessage]) -> AssistantMessage: pass
