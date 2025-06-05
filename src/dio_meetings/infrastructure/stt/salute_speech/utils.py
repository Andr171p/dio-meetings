from typing import Union

from pathlib import Path

from .constants import CONTENT_TYPE, AUDIO_ENCODING
from src.dio_meetings.utils import get_file_extension


CONTENT_TYPES_DICT: dict[str, CONTENT_TYPE] = {
    "mp3": "audio/mpeg",
    "ogg": "audio/ogg;codecs=opus"
}

AUDIO_ENCODING_DICT: dict[str,AUDIO_ENCODING] = {
    "pcm": "PCM_S16LE",
    "ogg": "OPUS",
    "mp3": "MP3",
    "fcal": "FLAC"
}


def get_content_type(file_path: Union[Path, str]) -> CONTENT_TYPE:
    file_extension = get_file_extension(file_path)
    content_type = CONTENT_TYPES_DICT.get(file_extension)
    if not content_type:
        raise ValueError("Unsupported file type")
    return content_type


def get_audio_encoding(file_extension: str) -> AUDIO_ENCODING:
    audio_encoding = AUDIO_ENCODING_DICT.get(file_extension)
    if not audio_encoding:
        raise ValueError("Unsupported file type")
    return audio_encoding
