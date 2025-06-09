import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

from .constants import ENV_PATH, SALUTE_SPEECH_SCOPE, PG_DRIVER


load_dotenv(ENV_PATH)


class SaluteSpeechSettings(BaseSettings):
    API_KEY: str = os.getenv("SALUTE_SPEECH_API_KEY")
    SCOPE: SALUTE_SPEECH_SCOPE = os.getenv("SALUTE_SPEECH_SCOPE")


class YandexGPTSettings(BaseSettings):
    FOLDER_ID: str = os.getenv("YANDEX_FOLDER_ID")
    API_KEY: str = os.getenv("YANDEX_GPT_API_KEY")


class MiniOSettings(BaseSettings):
    MINIO_URL: str = os.getenv("MINIO_URL")
    MINIO_USER: str = os.getenv("MINIO_USER")
    MINIO_PASSWORD: str = os.getenv("MINIO_PASSWORD")


class PostgresSettings(BaseSettings):
    PG_HOST: str = os.getenv("POSTGRES_HOST")
    PG_PORT: int = os.getenv("POSTGRES_PORT")
    PG_USER: str = os.getenv("POSTGRES_USER")
    PG_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    PG_DB: str = os.getenv("POSTGRES_DB")

    @property
    def sqlalchemy_url(self) -> str:
        return f"postgresql+{PG_DRIVER}://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


class RedisSettings(BaseSettings):
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


class Settings(BaseSettings):
    salute_speech: SaluteSpeechSettings = SaluteSpeechSettings()
    yandex_gpt: YandexGPTSettings = YandexGPTSettings()
    minio: MiniOSettings = MiniOSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
