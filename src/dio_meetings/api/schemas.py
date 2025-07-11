from typing import Annotated

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from fastapi import UploadFile, File, Query

AudioFile = Annotated[UploadFile, File(..., description="Аудио запись встречи/совещания")]

Date = Annotated[
    datetime,
    Query(
        ...,
        description="Дата для фильтрации в формате YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS",
        examples=["2025-01-01", "2025-01-01T12:00:00"]
    )
]

Page = Annotated[int, Query(description="Страница с метаданными")]

Limit = Annotated[
    int,
    Query(description="Лимит метаданных на одной странице")
]


class TaskCreateSchema(BaseModel):
    file_id: UUID
