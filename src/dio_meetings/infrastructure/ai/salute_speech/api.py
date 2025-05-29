from typing import Optional, Union

import json
import base64
import logging
from pathlib import Path
from uuid import UUID, uuid4

import aiohttp
import aiofiles

from .schemas import TaskResult, FinishedTaskResult, RecognizedText
from .exceptions import AuthorizationError, UploadError, TaskError, DownloadError
from .constants import (
    SALUTE_SPEECH_URL,
    SBER_DEVICES_URL,
    AVAILABLE_SCOPES,
    AVAILABLE_MODELS,
    SUPPORTED_LANGUAGES,
    ENABLE_LETTERS,
    EOU_TIMEOUT,
    # MAX_SPEECH_TIMEOUT,
    # NO_SPEECH_TIMEOUT,
    # HYPOTHESES_COUNT,
    STATUS_200_OK,
    STATUS_401_UNAUTHORIZED
)
from .utils import get_content_type, get_audio_encoding


class SberDevicesAPI:
    def __init__(
            self,
            api_key: Optional[str] = None,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            scope: AVAILABLE_SCOPES = "SALUTE_SPEECH_PERS",
            ssl_check: bool = False
    ) -> None:
        self._api_key = api_key
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope
        self._rq_uuid = str(uuid4())
        self._ssl_check = ssl_check

    def __create_api_key(self) -> str:
        credentials = f"{self._client_id}:{self._client_secret}"
        return base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    async def _authorize(self) -> Optional[str]:
        """Возвращает access token для авторизации"""
        url = f"{SBER_DEVICES_URL}/oauth"
        headers = {
            "Authorization": f"Basic {self._api_key if self._api_key else self.__create_api_key()}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": self._rq_uuid
        }
        payload = {"scope": self._scope}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=url,
                        headers=headers,
                        data=payload,
                        ssl=self._ssl_check
                ) as response:
                    if response.status == STATUS_401_UNAUTHORIZED:
                        return None
                    if response.status != STATUS_200_OK:
                        raise AuthorizationError(f"Auth failed with status {response.status}")
                    data = await response.json()
            return data["access_token"]
        except aiohttp.ClientError as e:
            raise AuthorizationError(f"Error while authorizations: {e}") from e


class SaluteSpeechAPI(SberDevicesAPI):
    def __init__(
            self,
            api_key: Optional[str] = None,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            scope: AVAILABLE_SCOPES = "SALUTE_SPEECH_PERS",
            ssl_check: bool = False,
            model: AVAILABLE_MODELS = "general",
            profanity_check: bool = False,
    ) -> None:
        super().__init__(
            api_key=api_key,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            ssl_check=ssl_check
        )
        self._logger = logging.getLogger(self.__class__.__name__)
        self._base_url = SALUTE_SPEECH_URL
        self._model = model
        self._profanity_check = profanity_check

    async def upload_file(self, file_path: Union[Path, str]) -> Optional[UUID]:
        url = f"{self._base_url}/data:upload"
        access_token = await self._authorize()
        content_type = get_content_type(file_path)
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": content_type,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with aiofiles.open(file_path, mode="rb") as file:
                    async with session.post(
                            url=url,
                            headers=headers,
                            data=file,
                            ssl=self._ssl_check
                    ) as response:
                        if response.status != STATUS_200_OK:
                            error_data = await response.json()
                            raise UploadError(
                                f"File upload failed. Status: {response.status}."
                                f"Error: {error_data}"
                            )
                        data = await response.json()
                        print(data)
            return UUID(data["result"]["request_file_id"])
        except aiohttp.ClientError as e:
            self._logger.error(f"Error while uploading file: {e}")
            raise UploadError(f"Error while uploading file: {e}") from e

    async def async_recognize(
            self,
            request_file_id: UUID,
            file_extension: str,
            language: SUPPORTED_LANGUAGES = "ru-RU",
            words: Optional[list[str]] = None
    ) -> Optional[TaskResult]:
        url = f"{self._base_url}/speech:async_recognize"
        access_token = await self._authorize()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        audio_encoding = get_audio_encoding(file_extension)
        payload = {
            "options": {
                "model": self._model,
                "audio_encoding": audio_encoding,
                "sample_rate": 16000,
                "language": language,
                "enable_profanity_filter": self._profanity_check,
                # "hypotheses_count": HYPOTHESES_COUNT,
                # "no_speech_timeout": NO_SPEECH_TIMEOUT,
                # "max_speech_timeout": MAX_SPEECH_TIMEOUT,
                "channels_count": 1,
                "speaker_separation_options": {
                    "enable": False,
                    "enable_only_main_speaker": False,
                    "count": 1
                },
                "insight_models": ["csi", "call_features"]
            },
            "request_file_id": str(request_file_id)
        }
        if words:
            payload["hints"] = {
                "words": words,
                "enable_letters": ENABLE_LETTERS,
                "eou_timeout": EOU_TIMEOUT
            }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=url,
                        headers=headers,
                        data=json.dumps(payload),
                        ssl=self._ssl_check
                ) as response:
                    data = await response.json()
            if data["status"] != STATUS_200_OK:
                raise TaskError(f"Task Error. Status: {data["status"]}")
            return TaskResult.model_validate(data["result"])
        except aiohttp.ClientError as e:
            self._logger.error(f"Error while async recognizing: {e}")
            raise TaskError(f"Error while async recognizing: {e}") from e

    async def get_task_status(
            self,
            task_id: UUID
    ) -> Optional[Union[TaskResult, FinishedTaskResult]]:
        url = f"{self._base_url}/task:get"
        access_token = await self._authorize()
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        params = {"id": str(task_id)}
        payload = {}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        url=url,
                        params=params,
                        headers=headers,
                        data=json.dumps(payload),
                        ssl=self._ssl_check
                ) as response:
                    data = await response.json()
            print(data)
            if data["status"] != STATUS_200_OK:
                raise TaskError(f"Task Error. Status: {data["status"]}")
            if data.get("response_file_id"):
                return FinishedTaskResult.model_validate(data["result"])
            return TaskResult.model_validate(data["result"])
        except aiohttp.ClientError as e:
            self._logger.error(f"Error while receiving task: {e}")
            raise TaskError(f"Error while receiving task: {e}") from e

    async def download_file(self, response_file_id: UUID) -> Optional[list[str]]:
        url = f"{SALUTE_SPEECH_URL}/data:download"
        access_token = await self._authorize()
        headers = {
            "Accept": "application/octet-stream",
            "Authorization": f"Bearer {access_token}"
        }
        params = {"response_file_id": str(response_file_id)}
        payload = {}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        url=url,
                        headers=headers,
                        params=params,
                        data=payload,
                        ssl=self._ssl_check
                ) as response:
                    if response.status != STATUS_200_OK:
                        error_data = await response.json()
                        raise DownloadError(
                            f"Download Error. Status: {response.status}. "
                            f"Error: {error_data}"
                        )
                    data = await response.text()
            results = json.loads(data)["result"]
            return [
                result["results"][0]["normalized_text"]
                for result in results
            ]
        except aiohttp.ClientError as e:
            self._logger.error(f"Error while downloading file: {e}")
            raise DownloadError(f"Error while downloading file: {e}") from e
