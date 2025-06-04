from typing import Any, Union

from abc import ABC, abstractmethod
from pathlib import Path

from .entities import BaseMessage, AssistantMessage


class BaseTranscripter(ABC):
    @abstractmethod
    async def transcript(self, file_path: Union[Path, str]) -> list[Any]: pass


class BaseLLM(ABC):
    @abstractmethod
    async def generate(self, messages: list[BaseMessage]) -> AssistantMessage: pass
