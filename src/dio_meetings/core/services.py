from typing import Union

from pathlib import Path

from .base import BaseTranscripter, BaseLLM
from .entities import SystemMessage, UserMessage

from ..template import PROTOCOL_TEMPLATE
from ..utils import get_transcriptions_text


class MeetingProtocolComposer:
    def __init__(
            self,
            transcripter: BaseTranscripter,
            llm: BaseLLM
    ) -> None:
        self._transcripter = transcripter
        self._llm = llm

    async def compose(self, file_path: Union[Path, str]) -> str:
        transcriptions = await self._transcripter.transcript(file_path)
        messages = [
            SystemMessage(text=PROTOCOL_TEMPLATE),
            UserMessage(text=get_transcriptions_text(transcriptions))
        ]
        assistant_message = await self._llm.generate(messages)
        return assistant_message.text
