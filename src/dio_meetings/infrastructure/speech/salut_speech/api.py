from typing import Optional, Union

import base64
import logging
from pathlib import Path
from uuid import UUID, uuid4

import aiohttp

from .schemas import CreatedTask
from .exceptions import AuthorizationError
from .constants import (
    SALUTE_SPEECH_URL,
    SBER_DEVICES_URL,
    AVAILABLE_SCOPES,
    STATUS_200_OK,
    STATUS_401_UNAUTHORIZED
)


class SberDevicesAPI:
    def __init__(
            self,
            api_key: Optional[str] = None,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            scope: AVAILABLE_SCOPES = "SALUTE_SPEECH_PERS"
    ) -> None:
        self._api_key = api_key
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope
        self._rq_uuid = str(uuid4())

    def __create_api_key(self) -> str:
        credentials = f"{self._client_id}:{self._client_secret}"
        return base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    async def _authorize(self) -> Optional[str]:
        """Возвращает access token для авторизации"""
        url = f"{SBER_DEVICES_URL}/oauth"
        headers = {
            "Authorization": f"Basic {self._api_key if self._api_key else self.__create_api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": self._rq_uuid
        }
        payload = {"scope": self._scope}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload, ssl=False) as response:
                    if response.status == STATUS_401_UNAUTHORIZED:
                        return None
                    if response.status != STATUS_200_OK:
                        print(await response.text())
                        raise AuthorizationError(f"Auth failed with status {response.status}")
                    data = await response.json()
            return data["access_token"]
        except aiohttp.ClientError as e:
            raise AuthorizationError(f"Error while authorizations: {e}") from e


class SalutSpeechAPI(SberDevicesAPI):
    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._base_url = SALUTE_SPEECH_URL

    async def upload_file(self, file_path: Union[Path, str]) -> Optional[UUID]:
        try:
            ...
        except ...:
            self._logger.error(...)

    async def async_recognize(self, request_file_id: UUID) -> CreatedTask:
        ...

    async def get_task_status(self, request_file_id: UUID) -> CreatedTask:
        ...
