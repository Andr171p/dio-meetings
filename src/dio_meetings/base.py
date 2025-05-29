from typing import Union

from abc import ABC, abstractmethod

from pathlib import Path


class BaseTranscripter(ABC):
    @abstractmethod
    async def transcript(self, file_path: Union[Path, str]) -> list[str]: pass
