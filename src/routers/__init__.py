__all__ = ("router",)

from fastapi import APIRouter

from .meeting_minutes import router as meeting_minutes_router
from .tasks import router as tasks_router

router = APIRouter(prefix="/api/v1")

router.include_router(meeting_minutes_router)
router.include_router(tasks_router)
