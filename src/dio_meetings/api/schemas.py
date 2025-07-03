from typing import Annotated

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from fastapi import UploadFile, File, Query

from ..core.base import Mode as FilterMode

from ..constants import START_PAGE, DEFAULT_LIMIT

AudioFile = Annotated[UploadFile, File(..., description="Аудио запись встречи/совещания")]

Date = Annotated[
    datetime,
    Query(
        ...,
        description="Дата для фильтрации в формате YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS",
        examples=["2025-01-01", "2025-01-01T12:00:00"]
    )
]

Mode = Annotated[
    FilterMode,
    Query(
        "after",
        description="Режим фильтрации: 'after' (после даты) или 'before' (до даты)"
    )
]

Page = Annotated[int, Query(START_PAGE, description="Страница с метаданными")]

Limit = Annotated[int, Query(DEFAULT_LIMIT, description="Лимит метаданных на одной странице")]


class TaskCreateSchema(BaseModel):
    file_id: UUID
