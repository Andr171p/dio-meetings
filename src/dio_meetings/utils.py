from typing import Union

from io import BytesIO
from uuid import uuid4
from pathlib import Path
from datetime import datetime

from pydub import AudioSegment


MS = 1000
DOCUMENT_PREFIX = "Протокол_совещания_"


def generate_file_name(format: str) -> str:
    return f"{uuid4()}.{format}"


def get_document_file_name(format: str) -> str:
    return f"{DOCUMENT_PREFIX}{datetime.now()}.{format}"


def get_file_format(file_path: Union[Path, str]) -> str:
    return file_path.split(".")[-1]


def get_audio_duration(audio_bytes: bytes, format: str) -> float:
    audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format=format)
    return len(audio_segment) / MS
