from typing import Annotated

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from fastapi import UploadFile, File, Query

from ..core.base import FilterMode

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
    str,
    Query(description="Режим фильтрации: 'after' (после даты) или 'before' (до даты)")
] = FilterMode.AFTER

Page = Annotated[int, Query(description="Страница с метаданными")] = START_PAGE

Limit = Annotated[
    int,
    Query(description="Лимит метаданных на одной странице")
] = DEFAULT_LIMIT


class TaskCreateSchema(BaseModel):
    file_id: UUID
