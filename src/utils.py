from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .schemas import AudioChunk

import io
import logging
from collections.abc import Iterator
from datetime import datetime

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from markdown_pdf import MarkdownPdf, Section
from pydub import AudioSegment
from pydub.utils import make_chunks

from .prompts import MEETING_MINUTES_PROMPT
from .settings import TIMEZONE, settings

logger = logging.getLogger(__name__)


def current_datetime() -> datetime:
    """Получение текущего времени в выбранном часовом поясе"""

    return datetime.now(TIMEZONE)


def get_audio_duration_ms(audio_file: bytes) -> float:
    """Получает длительность аудио в мили секундах"""

    audio = AudioSegment.from_file(audio_file)
    return audio.duration_seconds / 1000


def split_audio_into_chunks(
        audio_file: bytes,
        audio_format: str,
        chunk_duration_ms: int = 20 * 60 * 1000,
        output_format: str = "wav",
) -> Iterator["AudioChunk"]:
    """Разделяет аудио файл на фрагменты с заданной продолжительностью.

    :param audio_file: Байты аудио файла.
    :param audio_format: Формат аудио, например: 'wav', 'ogg', 'm4a'.
    :param chunk_duration_ms: Продолжительность сегмента в миллисекундах.
    :param output_format: Формат фрагмента аудио.
    :returns: Объекты аудио фрагментов.
    """

    from .schemas import AudioChunk  # noqa: PLC0415

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
            index=i,
            total_count=chunks_count,
            content=chunk_content,
            size_mb=round(len(chunk_content) / 1_000_000, 2),
            audio_format=output_format,
            duration_ms=chunk_duration_ms,
        )


async def generate_meeting_minutes(transcript: str) -> str:
    """Генерирует протокол совещания по его транскрибации.

    :param transcript: Транскрибация совещания.
    :returns: Составленный протокол в Markdown формате.
    """

    model = ChatOpenAI(
        api_key=settings.yandexcloud.api_key,
        model=settings.yandexcloud.qwen3_235b,
        base_url=settings.yandexcloud.llm_base_url,
        temperature=0.1,
        max_retries=3,
    )
    prompt = ChatPromptTemplate.from_template(MEETING_MINUTES_PROMPT)
    chain = prompt | model | StrOutputParser()
    return await chain.ainvoke({"transcript": transcript})


def md_to_pdf(md_text: str) -> bytes:
    """Формирует PDF файл по Markdown тексту"""

    pdf = MarkdownPdf()
    pdf.add_section(Section(md_text))
    buffer = io.BytesIO()
    pdf.save_bytes(buffer)
    return buffer.getvalue()
