import logging

from src.dio_meetings.api import create_fastapi_app


logging.basicConfig(level=logging.INFO)

app = create_fastapi_app()
