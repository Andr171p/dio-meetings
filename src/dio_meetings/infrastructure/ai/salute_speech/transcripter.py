from typing import Union

import asyncio
from pathlib import Path

from .api import SaluteSpeechAPI
from .constants import AVAILABLE_SCOPES, DEFAULT_ASYNC_TIMEOUT
from src.dio_meetings.base import BaseTranscripter
from src.dio_meetings.utils import get_file_extension


class SaluteSpeechTranscripter(BaseTranscripter):
    def __init__(
            self,
            api_key: str,
            scope: [AVAILABLE_SCOPES],
            async_timeout: int = DEFAULT_ASYNC_TIMEOUT
    ) -> None:
        self._salute_speech_api = SaluteSpeechAPI(api_key=api_key, scope=scope)
        self._async_timeout = async_timeout

    async def transcript(self, file_path: Union[Path, str]) -> list[str]:
        request_file_id = await self._salute_speech_api.upload_file(file_path)
        task_result = await self._salute_speech_api.async_recognize(
            request_file_id=request_file_id,
            file_extension=get_file_extension(file_path)
        )
        while task_result.status != "DONE":
            await asyncio.sleep(self._async_timeout)
            task_result = await self._salute_speech_api.get_task_status(task_result.id)
        response_file_id = task_result.response_file_id
        recognized_texts = await self._salute_speech_api.download_file(response_file_id)
        return recognized_texts
