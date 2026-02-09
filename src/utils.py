import io
import logging
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime

import ffmpeg
from markdown_pdf import MarkdownPdf, Section
from pydub import AudioSegment
from pydub.utils import make_chunks

from .settings import TIMEZONE

logger = logging.getLogger(__name__)


def current_datetime() -> datetime:
    """Получение текущего времени в выбранном часовом поясе"""

    return datetime.now(TIMEZONE)


def video_to_audio(
        video_file: bytes, video_format: str, output_format: str = "mp3"
) -> bytes:
    """Конвертирует видео в аудио.

    :param video_file: Исходное видео.
    :param video_format: Формат исходного видео.
    :param output_format: Выходной формат аудио, по умолчанию `mp3`.
    :returns: Байты аудио файла.
    """

    input_format = video_format.lstrip(".").lower()
    output_format = output_format.lstrip(".").lower()
    try:
        stream = ffmpeg.input("pipe:", format=input_format)
        stream = ffmpeg.output(
            stream,
            "pipe:",
            format=output_format,
            acodec="libmp3lame" if output_format == "mp3" else "copy",
            vn=True,
            loglevel="error",
        )
        process = (
            ffmpeg
            .run_async(
                stream, pipe_stdin=True, pipe_stdout=True, pipe_stderr=True,
            )
        )
        out, err = process.communicate(input=video_file)
        if process.returncode != 0:
            error_text = err.decode("utf-8", errors="replace").strip()
            raise RuntimeError(
                f"FFmpeg process finished with exit code {process.returncode}, error: {error_text}"
            ) from None
        if not out:
            raise ValueError("FFmpeg output is empty!")
    except ffmpeg.Error as e:
        error_detail = e.stderr.decode("utf-8", errors="replace") if e.stderr else str(e)
        raise RuntimeError(
            f"Error occurred while convert video to audio, ffmpeg error: {error_detail}"
        ) from e
    else:
        return out


def get_audio_duration(audio_file: bytes) -> float:
    """Получает длительность аудио в секундах"""

    audio = AudioSegment.from_file(audio_file)
    return audio.duration_seconds


def get_video_duration(video_file: bytes, video_format: str) -> float:
    """Получает длительность видео в секундах"""

    try:
        probe = ffmpeg.probe(
            "pipe:0",
            cmd="ffprobe",
            format=video_format,
            show_format=True,
            show_streams=False,
            stdin=video_file,
        )
        duration_str = probe.get("format", {}).get("duration")
        if duration_str is None:
            for stream in probe.get("streams", []):
                if "duration" in stream:
                    duration_str = stream["duration"]
                    break
        if duration_str is None:
            raise ValueError(
                "FFprobe could not determine the duration (no duration field in format/streams)"
            )
        return float(duration_str)
    except ffmpeg.Error as e:
        error_detail = e.stderr.decode("utf-8", errors="replace").strip() if e.stderr else str(e)
        raise RuntimeError(
            f"FFprobe error occurred while duration receipt:\n{error_detail}"
        ) from e


@dataclass
class AudioChunk:
    """Фрагмент аудио записи.

    Attributes:
        serial_number: Порядковый номер в последовательности.
        sequence_length: Длина последовательности всех чанков.
        content: Поток байтов.
        format: Аудио формат, например: 'wav', 'mp3', ...
        size_mb: Размер чанка в мега-байтах.
        duration: Длительность в секундах.
    """

    serial_number: int
    sequence_length: int
    content: bytes
    format: str
    size_mb: float
    duration: float


def split_audio_into_chunks(
        audio_file: bytes,
        audio_format: str,
        chunk_duration_ms: int = 20 * 60 * 1000,
        output_format: str = "wav",
) -> Iterator[AudioChunk]:
    """Разделяет аудио файл на фрагменты с заданной продолжительностью.

    :param audio_file: Байты аудио файла.
    :param audio_format: Формат аудио, например: 'wav', 'ogg', 'm4a'.
    :param chunk_duration_ms: Продолжительность сегмента в миллисекундах.
    :param output_format: Формат фрагмента аудио.
    :returns: Объекты аудио фрагментов.
    """

    logger.info("Start split audio into chunks...")
    audio = AudioSegment.from_file(io.BytesIO(audio_file), format=audio_format)
    chunks = make_chunks(audio, chunk_duration_ms)
    chunks_count = len(chunks)
    logger.info("Created %s chunks from audio", chunks_count)
    for i, chunk in enumerate(chunks):
        buffer = io.BytesIO()
        chunk.export(buffer, format=output_format, bitrate="256k")
        logger.info(
            "Export %s chunk content to %s format", i + 1, output_format.upper()
        )
        chunk_content = buffer.getvalue()
        yield AudioChunk(
            serial_number=i,
            sequence_length=chunks_count,
            content=chunk_content,
            format=output_format,
            size_mb=round(len(chunk_content) / 1_000_000, 2),
            duration=get_audio_duration(chunk_content),
        )


def md_to_pdf(md_text: str) -> bytes:
    """Формирует PDF файл по Markdown тексту"""

    pdf = MarkdownPdf()
    pdf.add_section(Section(md_text))
    buffer = io.BytesIO()
    pdf.save_bytes(buffer)
    return buffer.getvalue()
