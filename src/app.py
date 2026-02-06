from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .broker import app as faststream_app
from .database.base import create_tables
from .routers import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_tables()
    await faststream_app.broker.start()
    yield
    await faststream_app.broker.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
