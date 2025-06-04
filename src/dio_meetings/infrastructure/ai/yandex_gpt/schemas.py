from typing import Literal

from pydantic import BaseModel


MESSAGE_ROLE = Literal[
    "system",
    "user",
    "assistant"
]


class BaseMessage(BaseModel):
    role: MESSAGE_ROLE
    text: str


class SystemMessage(BaseMessage):
    role: MESSAGE_ROLE = "system"


class UserMessage(BaseMessage):
    role: MESSAGE_ROLE = "user"


class AssistantMessage(BaseMessage):
    role: MESSAGE_ROLE = "assistant"
