import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

from .constants import ENV_PATH, SALUTE_SPEECH_SCOPE


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


class Settings(BaseSettings):
    salute_speech: SaluteSpeechSettings = SaluteSpeechSettings()
    yandex_gpt: YandexGPTSettings = YandexGPTSettings()
    minio: MiniOSettings = MiniOSettings()
