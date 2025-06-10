from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka.integrations.fastapi import setup_dishka

from .lifespan import lifespan
from .routers import meetings_router, tasks_router, results_router

from ..ioc import container


def create_fastapi_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(meetings_router)
    app.include_router(tasks_router)
    app.include_router(results_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_dishka(app=app, container=container)
    return app
