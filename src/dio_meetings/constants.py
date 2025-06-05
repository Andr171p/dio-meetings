from pathlib import Path


# Директория проекта:
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Переменные окружения:
ENV_PATH = BASE_DIR / ".env"
