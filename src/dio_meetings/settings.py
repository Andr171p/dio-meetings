import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

from .constants import ENV_PATH


load_dotenv(ENV_PATH)


class SaluteSpeechSettings(BaseSettings):
    API_KEY: str = os.getenv("SALUTE_SPEECH_API_KEY")
    SCOPE: str = os.getenv("SALUTE_SPEECH_SCOPE")


class YandexGPTSettings(BaseSettings):
    FOLDER_ID: str = os.getenv("YANDEX_FOLDER_ID")
    API_KEY: str = os.getenv("YANDEX_GPT_API_KEY")


class Settings(BaseSettings):
    salute_speech: SaluteSpeechSettings = SaluteSpeechSettings()
    yandex_gpt: YandexGPTSettings = YandexGPTSettings()
