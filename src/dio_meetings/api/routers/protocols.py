from uuid import UUID

from fastapi import APIRouter, status


protocols_router = APIRouter(
    prefix="/api/v1/protocols",
    tags=["Protocols"]
)


@protocols_router.get(
    path="/{protocol_id}",
    status_code=status.HTTP_200_OK,
    response_model=...
)
async def get_protocol(protocol_id: UUID) -> ...:
    ...
