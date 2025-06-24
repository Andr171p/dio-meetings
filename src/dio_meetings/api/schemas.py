from uuid import UUID

from pydantic import BaseModel


class TaskCreateSchema(BaseModel):
    file_id: UUID
