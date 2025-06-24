from pydantic import BaseModel, ConfigDict

from .enums import Role, Emotion


class BaseMessage(BaseModel):
    role: Role
    text: str


class SystemMessage(BaseMessage):
    role: Role = Role.SYSTEM


class UserMessage(BaseMessage):
    role: Role = Role.USER


class AIMessage(BaseMessage):
    role: Role = Role.AI


class Transcription(BaseModel):
    text: str         # Транскрибированный текст
    speaker_id: int   # ID спикера
    emotion: Emotion  # Эмоция спикера

    model_config = ConfigDict(from_attributes=True)
