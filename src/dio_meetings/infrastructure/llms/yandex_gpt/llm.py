from .api import YandexGPTAPI
from .constants import MODELS, URL

from src.dio_meetings.core.base import BaseLLM
from src.dio_meetings.core.dto import BaseMessage, AIMessage


class YandexGPT(BaseLLM):
    def __init__(
            self,
            folder_id: str,
            api_key: str,
            model: MODELS = "yandexgpt"
    ) -> None:
        self._yandex_gpt_api = YandexGPTAPI(
            folder_id=folder_id,
            api_key=api_key,
            model=model,
            url=URL
        )

    async def generate(self, messages: list[BaseMessage]) -> AIMessage:
        response = await self._yandex_gpt_api.acomplete(
            messages=[message.model_dump() for message in messages]
        )
        alternative = response["result"]["alternatives"][0]
        return AIMessage(text=alternative["message"]["text"])
