from typing import Union

from io import BytesIO
from pathlib import Path

from pydub import AudioSegment


MS = 1000


def get_file_format(file_path: Union[Path, str]) -> str:
    return file_path.split(".")[-1]


def get_audio_duration(audio_bytes: bytes, format: str) -> float:
    audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format=format)
    return len(audio_segment) / MS
