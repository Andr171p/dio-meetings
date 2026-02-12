from typing import Literal

from pathlib import Path

import pytz
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

TIMEZONE = pytz.timezone("Europe/Moscow")
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

SQLITE_URL = f"sqlite+aiosqlite:///{BASE_DIR / "db.sqlite3"}"
CHROMA_PATH = BASE_DIR / ".chroma"
TEMP_DIR = BASE_DIR / ".temp"

load_dotenv(ENV_PATH)


class YandexCloudSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="YANDEX_CLOUD_")

    folder_id: str = "<FOLDER_ID>"
    api_key: str = "<API_KEY>"
    access_key_id: str = "<API_KEY_ID>"
    secret_access_key: str = "<SECRET_KEY>"
    llm_base_url: str = "https://llm.api.cloud.yandex.net/v1"

    @property
    def gemma_3_27b_it(self) -> str:
        return f"gpt://{self.folder_id}/gemma-3-27b-it/latest"

    @property
    def aliceai_llm(self) -> str:
        return f"gpt://{self.folder_id}/aliceai-llm"

    @property
    def qwen3_235b(self) -> str:
        return f"gpt://{self.folder_id}/qwen3-235b-a22b-fp8/latest"

    @property
    def yandexgpt_rc(self) -> str:
        return f"gpt://{self.folder_id}/yandexgpt/rc"


class SberDevicesSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SBER_DEVICES_")

    api_key: str = "<API_KEY>"
    scope: str = "<SCOPE>"
    client_id: str = "<CLIENT_ID>"
    client_secret: str = "<CLIENT_SECRET>"


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    host: str = "postgres"
    port: int = 5432
    user: str = "<USER>"
    password: str = "<PASSWORD>"
    db: str = "<DB>"
    driver: Literal["asyncpg"] = "asyncpg"

    @property
    def sqlalchemy_url(self) -> str:
        return f"postgresql+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    host: str = "redis"
    port: str = 6379

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/0"


class Settings(BaseSettings):
    yandexcloud: YandexCloudSettings = YandexCloudSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    sberdevices: SberDevicesSettings = SberDevicesSettings()


settings = Settings()
