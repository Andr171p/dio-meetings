from typing import Optional

from .api import YandexGPTAPI

from src.dio_meetings.base import BaseLLM
from src.dio_meetings.entities import BaseMessage, AssistantMessage


class YandexGPTLLM(BaseLLM):
    def __init__(
            self,
            folder_id: str,
            api_key: Optional[str] = None,
            iam_token: Optional[str] = None
    ) -> None:
        self._yandex_gpt_api = YandexGPTAPI(
            folder_id=folder_id,
            api_key=api_key,
            iam_token=iam_token
        )

    async def generate(self, messages: list[BaseMessage]) -> AssistantMessage:
        response = await self._yandex_gpt_api.acomplete(
            messages=[message.model_dump() for message in messages]
        )
        return AssistantMessage(text=response["result"]["alternatives"][0]["message"]["text"])
