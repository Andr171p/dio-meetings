from typing import Annotated

from fastapi import UploadFile, File, Form


AudioFile = Annotated[UploadFile, File(..., description="Аудио запись встречи/совещания")]

TitleForm = Annotated[str, Form(..., description="Тема/название совещания")]

ParticipantsForm = Annotated[list[str], Form(..., description="Список участников встречи")]
