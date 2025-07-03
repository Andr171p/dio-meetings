from typing import Optional

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .enums import FileType, TaskStatus

from ..constants import AUDIO_FORMATS, DOCUMENT_FORMATS


class File(BaseModel):
    data: bytes
    file_name: str

    @property
    def size(self) -> float:
        return round(len(self.data) / (1024 * 1024), 2)

    @property
    def format(self) -> str:
        return self.file_name.split(".")[-1]

    @property
    def type(self) -> FileType:
        if self.format in AUDIO_FORMATS:
            return FileType.AUDIO
        elif self.format in DOCUMENT_FORMATS:
            return FileType.DOCUMENT
        else:
            raise ValueError("Unsupported file format")


class FileMetadata(BaseModel):
    id: Optional[UUID] = None    # ID файла
    file_name: str               # Имя файла
    key: str                     # Ссылка на S3
    bucket: str                  # Имя бакета в S3
    size: float                  # Размер в МБ
    format: str                  # Формат файла / расширение
    type: FileType               # Тип файла
    uploaded_date: datetime      # Дата загрузки

    model_config = ConfigDict(from_attributes=True)


class Task(BaseModel):
    id: Optional[UUID] = None         # ID задачи
    file_id: UUID                     # Файл для распознавания
    status: TaskStatus                # Статус выполнения задачи
    result_id: Optional[UUID] = None  # ID сформированного файла

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
