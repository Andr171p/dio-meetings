from uuid import UUID

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import Response

from dishka.integrations.fastapi import DishkaRoute, FromDishka as Depends

from ..schemas import Date, Mode

from ...core.enums import FileType
from ...core.domain import FileMetadata
from ...core.services import FileService
from ...core.base import FileMetadataRepository

from ...constants import DOCUMENTS_BUCKET, NOT_FOUND

documents_router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
    route_class=DishkaRoute
)


@documents_router.get(
    path="/filter",
    status_code=status.HTTP_200_OK,
    response_model=list[FileMetadata],
    summary="Фильтрует документы по дате."
)
async def filter_document_by_date(
        date: Date,
        mode: Mode,
        file_metadata_repository: Depends[FileMetadataRepository]
) -> list[FileMetadata]:
    files_metadata = await file_metadata_repository.filter_by_date(
        date=date, type=FileType.DOCUMENT, mode=mode
    )
    return files_metadata


@documents_router.get(
    path="/{result_id}/download",
    status_code=status.HTTP_200_OK,
)
async def download_document(result_id: UUID, file_service: Depends[FileService]) -> Response:
    downloaded_file = await file_service.download(result_id, bucket=DOCUMENTS_BUCKET)
    if not downloaded_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return Response(
        content=downloaded_file.data,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{downloaded_file.file_name}",
            "Content-Length": str(len(downloaded_file.data)),
        }
    )


@documents_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[FileMetadata],
    summary="Получает список всех документов."
)
async def get_documents_list(
        file_metadata_repository: Depends[FileMetadataRepository]
) -> list[FileMetadata]:
    files_metadata = await file_metadata_repository.read_all(bucket=DOCUMENTS_BUCKET)
    return files_metadata
