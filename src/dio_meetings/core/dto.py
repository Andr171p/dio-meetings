from typing import Literal

import io
from uuid import UUID

from pydantic import BaseModel


ROLE = Literal[
    "system",
    "user",
    "ai"
]


EMOTION = Literal[
    "positive",
    "neutral",
    "negative"
]


class BaseMessage(BaseModel):
    role: ROLE
    text: str


class SystemMessage(BaseMessage):
    role: ROLE = "system"


class UserMessage(BaseMessage):
    role: ROLE = "user"


class AIMessage(BaseMessage):
    role: ROLE = "ai"


class Transcription(BaseModel):
    text: str  # Транскрибированный текст
    speaker_id: int  # ID спикера
    emotion: EMOTION  # Эмоция спикера


class BuiltDocument(BaseModel):
    document_id: UUID
    file_buffer: io.BytesIO
