from uuid import UUID

from pydantic import BaseModel


class Meeting(BaseModel):
    meeting_id: UUID
    title: str  # Название / тема встречи
    participants: list[str]  # Список участников встречи
    file_name: str


class MeetingProtocol(BaseModel):
    protocol_id: UUID
    title: str
    file_name: str
