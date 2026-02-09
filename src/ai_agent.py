from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .prompts import MINUTES_PROMPT
from .settings import settings


async def generate_minutes(transcript: str) -> str:
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
    prompt = ChatPromptTemplate.from_template(MINUTES_PROMPT)
    chain = prompt | model | StrOutputParser()
    return await chain.ainvoke({"transcript": transcript})
