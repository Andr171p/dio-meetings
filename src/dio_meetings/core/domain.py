from pydantic import BaseModel


class Meeting(BaseModel):
    title: str  # Название / тема встречи
    participants: list[str]  # Список участников встречи
    file_path: str


class MeetingProtocol(BaseModel):
    title: str
    file_path: str
