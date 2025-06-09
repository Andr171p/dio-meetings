from fastapi import APIRouter, status, HTTPException
from fastapi.responses import Response

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ...core.base import FileRepository
from ...core.exceptions import DownloadError


protocols_router = APIRouter(
    prefix="/api/v1/protocols",
    tags=["Protocols"],
    route_class=DishkaRoute
)


@protocols_router.get(
    path="/{protocol_key}/download",
    status_code=status.HTTP_200_OK,
)
async def download_protocol(
        protocol_key: str,
        file_repository: FromDishka[FileRepository]
) -> Response:
    try:
        file_content = await file_repository.download_file(
            file_name=protocol_key,
            bucket_name="protocols"
        )
    except DownloadError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Protocol not found")
    return Response(
        content=file_content,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={protocol_key}"}
    )


@protocols_router.delete(
    path="/{protocol_key}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_protocol(
        protocol_key: str,
        file_repository: FromDishka[FileRepository]
) -> None:
    await file_repository.delete_file(
        file_name=protocol_key,
        bucket_name="protocols"
    )
