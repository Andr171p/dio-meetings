from typing import Union

from pathlib import Path

from .constants import AVAILABLE_CONTENT_TYPES, AVAILABLE_AUDIO_ENCODINGS
from src.dio_meetings.utils import get_file_extension


def get_content_type(file_path: Union[Path, str]) -> AVAILABLE_CONTENT_TYPES:
    file_extension = get_file_extension(file_path)
    match file_extension:
        case "mp3":
            return "audio/mpeg"
        case "ogg":
            return ...
        case _:
            raise ValueError("Unsupported file")


def get_audio_encoding(file_extension: str) -> AVAILABLE_AUDIO_ENCODINGS:
    match file_extension:
        case "pcm":
            return "PCM_S16LE"
        case "ogg":
            return "OPUS"
        case "mp3":
            return "MP3"
        case "flac":
            return "FLAC"
        case _:
            raise ValueError("Unsupported file")
