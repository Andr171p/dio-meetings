from typing import Union

import asyncio
import io

from .api import SaluteSpeechAPI
from .constants import SCOPE, DEFAULT_ASYNC_TIMEOUT

from src.dio_meetings.core.base import STTService
from src.dio_meetings.core.dto import Transcription


class SaluteSpeechService(STTService):
    def __init__(
            self,
            api_key: str,
            scope: SCOPE,
            async_timeout: int = DEFAULT_ASYNC_TIMEOUT
    ) -> None:
        self._salute_speech_api = SaluteSpeechAPI(api_key=api_key, scope=scope)
        self._async_timeout = async_timeout

    async def transcript(
            self,
            audio_file: Union[io.BytesIO, bytes],
            file_format: str
    ) -> list[Transcription]:
        request_file_id = await self._salute_speech_api.upload_file(audio_file, file_format)
        task_result = await self._salute_speech_api.async_recognize(
            request_file_id=request_file_id,
            file_extension=file_format
        )
        while task_result.status != "DONE":
            await asyncio.sleep(self._async_timeout)
            task_result = await self._salute_speech_api.get_task_status(task_result.id)
        response_file_id = task_result.response_file_id
        recognized_results = await self._salute_speech_api.download_file(response_file_id)
        return [
            Transcription.model_validate(recognized_result.model_dump())
            for recognized_result in recognized_results
        ]
