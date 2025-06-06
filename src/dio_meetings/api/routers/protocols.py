from uuid import UUID

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import StreamingResponse

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ...core.base import FileRepository


protocols_router = APIRouter(
    prefix="/api/v1/protocols",
    tags=["Protocols"],
    route_class=DishkaRoute
)


@protocols_router.get(
    path="/{protocol_id}/download",
    status_code=status.HTTP_200_OK,
)
async def get_protocol(
        protocol_id: UUID,
        file_repository: FromDishka[FileRepository]
) -> StreamingResponse:
    file_content = await file_repository.download_file(
        file_name=protocol_id,
        bucket_name="protocols"
    )
    if not file_content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Protocol not found")
    return StreamingResponse(
        content=file_content,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={protocol_id}"}
    )
