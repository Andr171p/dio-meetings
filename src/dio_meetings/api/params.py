from typing import Annotated, Literal, Optional

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from fastapi import UploadFile, File, Form


AudioFile = Annotated[UploadFile, File(..., description="Аудио запись встречи/совещания")]

TitleForm = Annotated[str, Form(..., description="Тема/название совещания")]

ParticipantsForm = Annotated[list[str], Form(..., description="Список участников встречи")]
