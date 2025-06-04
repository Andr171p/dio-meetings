from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka.integrations.fastapi import setup_dishka

from ..ioc import container
from .routers import meetings_router, protocols_router


def create_fastapi_app() -> FastAPI:
    app = FastAPI()
    app.include_router(meetings_router)
    app.include_router(protocols_router)
    setup_dishka(app=app, container=container)
    return app
