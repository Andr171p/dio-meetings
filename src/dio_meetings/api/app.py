from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka.integrations.fastapi import setup_dishka

from ..ioc import container
from .routers import meetings_router, tasks_router, protocols_router


def create_fastapi_app() -> FastAPI:
    app = FastAPI()
    app.include_router(meetings_router)
    app.include_router(tasks_router)
    app.include_router(protocols_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_dishka(app=app, container=container)
    return app
