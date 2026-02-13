import contextlib
import logging
import os
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

import aiofiles.tempfile
import anyio
import ffmpeg
from pydub import AudioSegment
from pydub.utils import make_chunks
from tinytag import TinyTag

BYTES_IN_MB = 1_000_000

logger = logging.getLogger(__name__)


async def convert_video_to_audio(
        input_path: str | Path,
        output_format: str = "mp3",
        *,
        temp_dir: str | None = None,
        cleanup: bool = True,
) -> bytes:
    """Конвертирует видео в аудио.

    :param input_path: Файл с исходным видео.
    :param output_format: Выходной формат аудио, по умолчанию `mp3`.
    :param temp_dir: Папка для временного аудио-файла (по умолчанию — системный temp).
    :param cleanup: Удалять ли временный файл после чтения (рекомендуется True)
    :returns: Байты аудио файла.
    """

    output_format = output_format.lstrip(".").lower()
    # Определение аудио кодек в зависимости от формата
    if output_format == "mp3":
        acodec = "libmp3lame"
    elif output_format in {"aac", "m4a"}:
        acodec = "aac"
    elif output_format == "wav":
        acodec = "pcm_s16le"
    else:
        acodec = "copy"

    async with aiofiles.tempfile.NamedTemporaryFile(
        suffix=f".{output_format}", dir=temp_dir, delete=False
    ) as tmp_file:
        output_path = tmp_file.name
        try:
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(
                stream,
                output_path,
                format=output_format,
                acodec=acodec,
                vn=True,
                loglevel="error",
            )
            process = ffmpeg.run_async(
                stream,
                pipe_stdout=False,
                pipe_stderr=True,
                overwrite_output=True,
            )
            _, err = process.communicate()
            if process.returncode != 0:
                error_text = err.decode("utf-8", errors="replace").strip() if err else ""
                raise RuntimeError(
                    f"FFmpeg failed with code {process.returncode}. "
                    f"Error: {error_text}\n"
                    f"Input: {input_path}\n"
                    f"Output format: {output_format}"
                )
            async with aiofiles.open(output_path, mode="rb") as file:
                content = await file.read()
            if not content:
                raise ValueError("FFmpeg produced empty output file!")
        except ffmpeg.Error as e:
            error_detail = (
                e.stderr.decode("utf-8", errors="replace").strip() if e.stderr else str(e)
            )
            raise RuntimeError(
                f"FFmpeg error during video to audio conversion: {error_detail}"
            ) from e
        else:
            return content
        finally:
            if cleanup and await anyio.Path(output_path).exists():
                with contextlib.suppress(OSError):
                    os.unlink(output_path)


@dataclass
class AudioChunk:
    """Фрагмент аудио записи.

    Attributes:
        serial_number: Порядковый номер в последовательности.
        sequence_length: Длина последовательности всех чанков.
        file_path: Путь до файла.
        format: Аудио формат, например: 'wav', 'mp3', ...
        size_mb: Размер чанка в мега-байтах.
        duration: Длительность в секундах.
    """

    serial_number: int
    sequence_length: int
    file_path: Path
    format: str
    size_mb: float
    duration: float


def split_audio_into_chunks(
        audio_file_path: str | Path,
        chunk_duration_ms: int = 20 * 60 * 1000,
        output_format: str = "wav",
        output_dir: str | Path = "chunks",
) -> Iterator[AudioChunk]:
    """Разделяет аудио файл на фрагменты с заданной продолжительностью.

    :param audio_file_path: Входной аудио файл.
    :param chunk_duration_ms: Продолжительность сегмента в миллисекундах.
    :param output_format: Формат фрагмента аудио.
    :param output_dir: Директория с выходными фрагментами.
    :returns: Объекты аудио фрагментов.
    """

    logger.info("Start split audio into chunks...")
    audio_format = str(audio_file_path).rsplit(".", maxsplit=1)[-1].lower()
    audio = AudioSegment.from_file(audio_file_path, format=audio_format)
    chunks = make_chunks(audio, chunk_duration_ms)
    chunks_count = len(chunks)
    logger.info("Created %s chunks from audio", chunks_count)
    for i, chunk in enumerate(chunks):
        chunk_file_path = output_dir / f"chunk_{i}_{uuid4().hex}.{output_format}"
        chunk.export(chunk_file_path, format=output_format, bitrate="256k")
        logger.info(
            "Export `%s` chunk to %s format", chunk_file_path, output_format.upper()
        )
        tag = TinyTag.get(chunk_file_path)
        size_md = round(tag.filesize / BYTES_IN_MB, 2)
        yield AudioChunk(
            serial_number=i,
            sequence_length=chunks_count,
            file_path=chunk_file_path,
            format=output_format,
            size_mb=size_md,
            duration=tag.duration,
        )


def get_media_duration(file_path: str | Path) -> float:
    """Получение длительности медиа контента в секундах"""

    try:
        logger.info("Start getting media file duration `%s` ...", file_path)
        probe = ffmpeg.probe(file_path)
        duration_str = probe.get("format", {}).get("duration")
        logger.info("Duration of media file `%s` - %s seconds", file_path, duration_str)
        if duration_str is not None:
            return float(duration_str)
        for stream in probe.get("streams", []):
            if "duration" in stream:
                return float(stream["duration"])
    except ffmpeg.Error as e:
        error_msg = e.stderr.decode("utf-8", errors="replace") if e.stderr else str(e)
        raise RuntimeError(f"FFprobe error: {error_msg}") from e
