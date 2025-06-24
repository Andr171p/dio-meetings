from uuid import UUID

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import Response

from dishka.integrations.fastapi import DishkaRoute, FromDishka as Depends

from ...core.domain import FileMetadata
from ...core.services import FileService
from ...core.base import FileMetadataRepository

from ...constants import DOCUMENTS_BUCKET


documents_router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
    route_class=DishkaRoute
)


@documents_router.get(
    path="/{result_id}/download",
    status_code=status.HTTP_200_OK,
)
async def download_document(result_id: UUID, file_service: Depends[FileService]) -> Response:
    downloaded_file = await file_service.download(result_id, bucket=DOCUMENTS_BUCKET)
    if not downloaded_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found")
    return Response(
        content=downloaded_file.data,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{downloaded_file.file_name}",
            "Content-Length": str(len(downloaded_file.data)),
        }
    )


@documents_router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[FileMetadata]
)
async def get_documents_list(
        file_metadata_repository: Depends[FileMetadataRepository]
) -> list[FileMetadata]:
    documents = await file_metadata_repository.read_all(bucket=DOCUMENTS_BUCKET)
    if not documents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No documents yet")
    return documents
