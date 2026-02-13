__all__ = ["router"]

from fastapi import APIRouter

from .meetings import router as meeting_router
from .minutes import router as minutes_router
from .tasks import router as tasks_router

router = APIRouter(prefix="/api/v2")

router.include_router(meeting_router)
router.include_router(tasks_router)
router.include_router(minutes_router)
