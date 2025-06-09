from faststream import FastStream
from faststream.redis import RedisBroker

from dishka.integrations.faststream import setup_dishka

from .router import meetings_router

from ...ioc import container


async def create_faststream_app() -> FastStream:
    broker = await container.get(RedisBroker)
    broker.include_router(meetings_router)
    app = FastStream(broker)
    setup_dishka(app=app, container=container, auto_inject=True)
    return app
