from typing import Literal

from pathlib import Path


# Директория проекта:
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Переменные окружения:
ENV_PATH = BASE_DIR / ".env"


PG_DRIVER: Literal["asyncpg"] = "asyncpg"


SALUTE_SPEECH_SCOPE = Literal[
    "SALUTE_SPEECH_PERS",
    "SALUTE_SPEECH_CORP"
]

BUCKET_NAME = "meeting-protocols"


# Поддерживаемые форматы аудио:
SUPPORTED_AUDIO_FORMATS = [
    "mp3",
    "ogg"
]

# Статусы выполнения задачи:
TASK_STATUS = Literal[
    "NEW",
    "RUNNING",
    "DONE",
    "ERROR"
]

# Имена s3 бакетов для хранения объектов:
MEETINGS_BUCKET_NAME = "meetings"
PROTOCOLS_BUCKET_NAME = "protocols"
