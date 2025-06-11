from uuid import UUID

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import Response

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ...core.services import TaskService


results_router = APIRouter(
    prefix="/api/v1/results",
    tags=["Results"],
    route_class=DishkaRoute
)


@results_router.get(
    path="/{result_id}/download",
    status_code=status.HTTP_200_OK,
)
async def download_result(result_id: UUID, task_service: FromDishka[TaskService]) -> Response:
    downloaded_file = await task_service.download_result(result_id)
    if not downloaded_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found")
    return Response(
        content=downloaded_file.file_data,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{downloaded_file.file_name}",
            "Content-Length": str(len(downloaded_file.file_data)),
        }
    )
