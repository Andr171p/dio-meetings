from langchain_gigachat import GigaChat

from src.dio_meetings.core.base import BaseLLM
from src.dio_meetings.core.dto import BaseMessage, AIMessage

LANGCHAIN_ROLES_MAPPING = {"system": "system", "user": "human", "ai": "ai"}


class GigaChatLLM(BaseLLM):
    def __init__(self, api_key: str, scope: str, model: str) -> None:
        self.giga_chat = GigaChat(
            credentials=api_key,
            scope=scope,
            model=model,
            profanity_check=False,
            verify_ssl_certs=False
        )

    async def generate(self, messages: list[BaseMessage]) -> AIMessage:
        response = await self.giga_chat.ainvoke(self._format_messages(messages))
        return AIMessage(text=response.content)

    @staticmethod
    def _format_messages(messages: list[BaseMessage]) -> list[dict[str, str]]:
        return [
            {"role": LANGCHAIN_ROLES_MAPPING[message.role], "content": message.text}
            for message in messages
        ]
