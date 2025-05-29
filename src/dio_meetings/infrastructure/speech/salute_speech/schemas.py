from typing import Literal, Union

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class TaskResult(BaseModel):
    id: Union[UUID, str]  # Идентификатор задачи
    created_at: datetime  # Дата создания задачи
    updated_at: datetime  # Дата обновления статуса задачи
    status: Literal[
        "NEW",
        "RUNNING",
        "CANCELED",
        "DONE",
        "ERROR"
    ]  # статус задачи
