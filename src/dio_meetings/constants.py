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

# Поддерживаемые форматы файлов:
AUDIO_FORMATS = [
    "mp3",
    "ogg",
    "pcm"
]
DOCUMENT_FORMATS = [
    "doc",
    "docx",
    "pdf"
]

# Имена s3 бакетов для хранения объектов:
AUDIO_BUCKET = "audio"
DOCUMENTS_BUCKET = "documents"

# Пагинация
START_PAGE = 1
DEFAULT_LIMIT = 5

# API ошибки
NOT_CREATED = "NOT_CREATED"
NOT_FOUND = "NOT_FOUND"
UPLOADING_ERROR = "UPLOADING_ERROR"
DOWNLOADING_ERROR = "DOWNLOADING_ERROR"
DELETION_ERROR = "DELETION_ERROR"
RECEIVING_ERROR = "RECEIVING_ERROR"
NOT_FILES_YET = "NOT_FILES_YET"
