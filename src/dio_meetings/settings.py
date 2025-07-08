import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

from .constants import ENV_PATH, PG_DRIVER

load_dotenv(ENV_PATH)


class RedisSettings(BaseSettings):
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


class PostgresSettings(BaseSettings):
    PG_HOST: str = os.getenv("POSTGRES_HOST")
    PG_PORT: int = os.getenv("POSTGRES_PORT")
    PG_USER: str = os.getenv("POSTGRES_USER")
    PG_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    PG_DB: str = os.getenv("POSTGRES_DB")

    @property
    def sqlalchemy_url(self) -> str:
        return f"postgresql+{PG_DRIVER}://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


class MinioSettings(BaseSettings):
    MINIO_URL: str = os.getenv("MINIO_URL")
    MINIO_USER: str = os.getenv("MINIO_USER")
    MINIO_PASSWORD: str = os.getenv("MINIO_PASSWORD")


class YandexGPTSettings(BaseSettings):
    FOLDER_ID: str = os.getenv("YANDEX_FOLDER_ID")
    API_KEY: str = os.getenv("YANDEX_GPT_API_KEY")


class GigaChatSettings(BaseSettings):
    API_KEY: str = os.getenv("GIGACHAT_API_KEY")
    SCOPE: str = os.getenv("GIGACHAT_SCOPE")
    MODEL_NAME: str = os.getenv("GIGACHAT_MODEL_NAME")


class SaluteSpeechSettings(BaseSettings):
    SCOPE: str = os.getenv("SALUTE_SPEECH_SCOPE")
    API_KEY: str = os.getenv("SALUTE_SPEECH_API_KEY")


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    minio: MinioSettings = MinioSettings()
    yandex_gpt: YandexGPTSettings = YandexGPTSettings()
    giga_chat: GigaChatSettings = GigaChatSettings()
    salute_speech: SaluteSpeechSettings = SaluteSpeechSettings()