from uuid import UUID

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import Response

from dishka.integrations.fastapi import DishkaRoute, FromDishka as Depends

from ..schemas import AudioFile, Date, Page, Limit

from ...core.base import FileMetadataRepository
from ...core.services import FileService
from ...core.enums import FileType
from ...core.domain import FileMetadata, File
from ...utils import convert_video_to_audio, get_file_format
from ...core.exceptions import (
    CreationError,
    ReadingError,
    UploadingError,
    DownloadingError,
    DeletingError,
    FileStoreError
)

from ...constants import (
    AUDIO_BUCKET,
    NOT_CREATED,
    UPLOADING_ERROR,
    DOWNLOADING_ERROR,
    NOT_FOUND,
    DELETION_ERROR,
    RECEIVING_ERROR,
    NOT_FILES_YET,
    VIDEO_FORMATS
)

audio_router = APIRouter(
    prefix="/api/v1/audio",
    tags=["Audio records"],
    route_class=DishkaRoute
)


@audio_router.post(
    path="/upload", 
    status_code=status.HTTP_201_CREATED,
    response_model=FileMetadata,
    summary="Загружает аудио запись совещания."
)
async def upload_audio(
        audio_file: AudioFile,
        file_service: Depends[FileService]
) -> FileMetadata:
    try:
        file_name = audio_file.filename
        file_format = get_file_format(file_name)
        if file_format in VIDEO_FORMATS:
            file_data = convert_video_to_audio(video_bytes=await audio_file.read())
            file_name = file_name.replace(file_format, "mp3")
        else:
            file_data = await audio_file.read()
        file = File(data=file_data, file_name=file_name)
        file_metadata = await file_service.upload(file, bucket=AUDIO_BUCKET)
        if not file_metadata:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=NOT_CREATED
            )
        return file_metadata
    except (CreationError, UploadingError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UPLOADING_ERROR
        )


@audio_router.get(
    path="/{file_id}/download",
    status_code=status.HTTP_200_OK,
    summary="Скачивает аудио запись совещания."
)
async def download_audio(
        file_id: UUID,
        file_service: Depends[FileService]
) -> Response:
    try:
        downloaded_file = await file_service.download(file_id, bucket=AUDIO_BUCKET)
        if not downloaded_file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return Response(
            content=downloaded_file.data,
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"inline; filename={downloaded_file.file_name}"}
        )
    except (ReadingError, DownloadingError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=DOWNLOADING_ERROR
        )


@audio_router.get(
    path="/filter",
    status_code=status.HTTP_200_OK,
    response_model=list[FileMetadata],
    summary="Фильтрует метаданные аудиозаписей по диапазону дат."
)
async def filter_audio_by_date_range(
        start: Date,
        end: Date,
        file_metadata_repository: Depends[FileMetadataRepository]
) -> list[FileMetadata]:
    try:
        files_metadata = await file_metadata_repository.filter_by_date_range(
            start_date=start, end_date=end, type=FileType.AUDIO
        )
        return files_metadata
    except ReadingError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=RECEIVING_ERROR
        )


@audio_router.get(
    path="/today",
    status_code=status.HTTP_200_OK,
    summary="Получает метаданные сегодняшних аудиозаписей."
)
async def get_today_audio(
        file_metadata_repository: Depends[FileMetadataRepository]
) -> list[FileMetadata]:
    try:
        files_metadata = await file_metadata_repository.get_today(type=FileType.AUDIO)
        return files_metadata
    except ReadingError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=RECEIVING_ERROR
        )


@audio_router.delete(
    path="/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаляет аудио запись совещания."
)
async def delete_audio(
        file_id: UUID,
        file_service: Depends[FileService]
) -> Response:
    try:
        is_deleted = await file_service.remove(file_id, bucket=AUDIO_BUCKET)
        if not is_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except (DeletingError, FileStoreError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=DELETION_ERROR
        )


@audio_router.get(
    path="/{file_id}/document",
    status_code=status.HTTP_200_OK,
    response_model=FileMetadata,
    summary="Получает документ распознанной аудиозаписи."
)
async def get_document_by_audio(
        file_id: UUID,
        file_metadata_repository: Depends[FileMetadataRepository]
) -> FileMetadata:
    try:
        file_metadata = await file_metadata_repository.get_result(file_id)
        if not file_metadata:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return file_metadata
    except ReadingError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=RECEIVING_ERROR
        )


@audio_router.get(
    path="/{file_id}",
    status_code=status.HTTP_200_OK,
    response_model=FileMetadata,
    summary="Получает метаданные аудио записи совещания."
)
async def get_audio(
        file_id: UUID,
        file_repository: Depends[FileMetadataRepository]
) -> FileMetadata:
    try:
        file_metadata = await file_repository.read(file_id)
        if not file_metadata:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return file_metadata
    except ReadingError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=RECEIVING_ERROR
        )


@audio_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[FileMetadata],
    summary="Получает список всех метаданные аудио записей совещаний."
)
async def get_audio_list(
        page: Page,
        limit: Limit,
        file_metadata_repository: Depends[FileMetadataRepository]
) -> list[FileMetadata]:
    try:
        files_metadata = await file_metadata_repository.read_all(
            page=page,
            limit=limit,
            bucket=AUDIO_BUCKET
        )
        if not files_metadata:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FILES_YET)
        return files_metadata
    except ReadingError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=RECEIVING_ERROR
        )
