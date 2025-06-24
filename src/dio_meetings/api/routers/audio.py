from typing import Annotated

from uuid import UUID

from fastapi import APIRouter, status, HTTPException, UploadFile, File
from fastapi.responses import Response

from dishka.integrations.fastapi import DishkaRoute, FromDishka as Depends

from ...core.base import FileMetadataRepository
from ...core.services import FileService
from ...core.domain import FileMetadata, File as AudioFile

from ...constants import AUDIO_BUCKET


audio_router = APIRouter(
    prefix="/api/v1/audio",
    tags=["Audio records"],
    route_class=DishkaRoute
)


@audio_router.post(
    path="/upload", 
    status_code=status.HTTP_201_CREATED,
    response_model=FileMetadata
)
async def upload_audio(
        audio_file: Annotated[UploadFile, File(..., description="Аудио запись встречи/совещания")],
        file_service: Depends[FileService]
) -> FileMetadata:
    file = AudioFile(data=await audio_file.read(), file_name=audio_file.filename)
    file_metadata = await file_service.upload(file, bucket=AUDIO_BUCKET)
    if not file_metadata:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while uploading audio file"
        )
    return file_metadata


@audio_router.get(
    path="/{file_id}/download",
    status_code=status.HTTP_200_OK
)
async def download_audio(
        file_id: UUID,
        file_service: Depends[FileService]
) -> Response:
    downloaded_file = await file_service.download(file_id, bucket=AUDIO_BUCKET)
    if not downloaded_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return Response(
        content=downloaded_file.data,
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"inline; filename={downloaded_file.file_name}"}
    )


@audio_router.delete(
    path="/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_audio(
        file_id: UUID,
        file_service: Depends[FileService]
) -> Response:
    is_deleted = await file_service.remove(file_id, bucket=AUDIO_BUCKET)
    if not is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@audio_router.get(
    path="/{file_id}",
    status_code=status.HTTP_200_OK,
    response_model=FileMetadata
)
async def get_audio(
        file_id: UUID,
        file_repository: Depends[FileMetadataRepository]
) -> FileMetadata:
    file_metadata = await file_repository.read(file_id)
    if not file_metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return file_metadata


@audio_router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[FileMetadata]
)
async def get_audio_list(
        file_metadata_repository: Depends[FileMetadataRepository]
) -> list[FileMetadata]:
    files_metadata = await file_metadata_repository.read_all(bucket=AUDIO_BUCKET)
    if not files_metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No files yet")
    return files_metadata
