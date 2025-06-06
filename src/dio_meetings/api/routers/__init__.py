__all__ = (
    "tasks_router",
    "meetings_router",
    "protocols_router"
)

from tasks import tasks_router
from .meetings import meetings_router
from .protocols import protocols_router
