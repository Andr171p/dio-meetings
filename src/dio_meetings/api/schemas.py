from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class AcceptedMeeting(BaseModel):
    task_id: UUID
    created_at: datetime
