from typing import Union

import io
import subprocess
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


def convert_video_to_audio(video_bytes: bytes) -> bytes:
    video_stream = io.BytesIO(video_bytes)
    audio_stream = io.BytesIO()
    try:
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", "pipe:0",  # Вход из stdin
            "-f", "mp3",     # Формат вывода - MP3
            "-ac", "2",      # 2 аудиоканала (стерео)
            "-ar", "44100",  # Частота дискретизации 44.1 kHz
            "-b:a", "192k",  # Бит-рейт 192 kbps
            "-vn",           # Игнорировать видео поток
            "pipe:1"         # Вывод в stdout
        ]
        process = subprocess.Popen(
            ffmpeg_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        audio_bytes, stderr = process.communicate(input=video_bytes)
        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {stderr.decode("utf-8")}")
        return audio_bytes
    except Exception as e:
        raise RuntimeError(f"Audio conversion failed: {e}") from e
    finally:
        video_stream.close()
        audio_stream.close()
