__all__ = ("router",)

from fastapi import APIRouter

from .audio import audio_router
from .tasks import tasks_router
from .documents import documents_router

router = APIRouter()

router.include_router(audio_router)
router.include_router(tasks_router)
router.include_router(documents_router)
