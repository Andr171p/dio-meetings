from typing import Union

from pathlib import Path

from .core.entities import Transcription


def get_file_extension(file_path: Union[Path, str]) -> str:
    return file_path.split(".")[-1]


def get_transcriptions_text(transcriptions: list[Transcription]) -> str:
    return "\n\n".join([
        f"(text: {transcription.text}, "
        f"speaker_id: {transcription.speaker_id}, "
        f"emotion: {transcription.emotion})"
        for transcription in transcriptions
    ])
