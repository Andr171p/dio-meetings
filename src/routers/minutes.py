from typing import Literal

from urllib.parse import quote
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response

from ..database.repositories import MinutesRepository
from ..dependencies import get_minutes_repo
from ..schemas import Minutes
from ..utils.docs import md_text_to_pdf

router = APIRouter(prefix="/minutes", tags=["Minutes"])


@router.get(
    path="/{meeting_id}",
    status_code=status.HTTP_200_OK,
    response_model=Minutes,
    summary="Получение протокола совещания",
)
async def get_minutes(
        meeting_id: UUID, repository: MinutesRepository = Depends(get_minutes_repo)
) -> Minutes:
    minutes = await repository.get_by_meeting(meeting_id)
    if minutes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MINUTES_NOT_FOUND")
    return minutes


@router.get(
    path="/{meeting_id}/download",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    summary="Скачать протокол совещания"
)
async def download_minutes(
        meeting_id: UUID,
        extension: Literal["pdf", "docx", "md"] = Query(..., description="Формат файла"),
        repository: MinutesRepository = Depends(get_minutes_repo),
) -> Response:
    minutes = await repository.get_by_meeting(meeting_id)
    if minutes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MINUTES_NOT_FOUND")
    md_text = minutes.md_text.replace("```", "").replace("markdown", "")
    match extension:
        case "pdf":
            content = md_text_to_pdf(md_text)
            filename = quote("Протокол_совещания.pdf")
            return Response(
                content=content,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename*=UTF-8''{filename}"
                },
            )
