from uuid import UUID

from pydantic import BaseModel


class TaskCreateSchema(BaseModel):
    meeting_id: UUID
