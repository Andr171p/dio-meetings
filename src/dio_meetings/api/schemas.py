from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class AcceptedMeeting(BaseModel):
    meeting_id: UUID
    task_id: UUID
    created_at: datetime
