from typing import Literal

from pathlib import Path


# Директория проекта:
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Переменные окружения:
ENV_PATH = BASE_DIR / ".env"

# Драйверы для работы с Postgres
PG_DRIVER: Literal["asyncpg"] = "asyncpg"


SALUTE_SPEECH_SCOPE = Literal[
    "SALUTE_SPEECH_PERS",
    "SALUTE_SPEECH_CORP"
]

# Эмоции распознанные при транскрибации
EMOTION = Literal[
    "positive",
    "neutral",
    "negative"
]

# Количество спикеров по умолчанию
SPEAKERS_COUNT = 6

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
MEETING_BUCKET_NAME = "meetings"
RESULT_BUCKET_NAME = "results"
