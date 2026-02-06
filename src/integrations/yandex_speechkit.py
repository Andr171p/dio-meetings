from typing import Any, Literal

import asyncio
import base64
import logging
import time

import aiohttp

from ..settings import settings

logger = logging.getLogger(__name__)

BASE_URL = "https://stt.api.cloud.yandex.net/"
OPERATION_URL = "https://operation.api.cloud.yandex.net/"


async def create_recognition_task(
        wav_file: bytes, sample_rate: Literal[8000, 16000, 48000] = 16000
) -> dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {settings.yandexcloud.api_key}"
    }
    payload = {
        "content": base64.b64encode(wav_file).decode("utf-8"),
        "recognitionModel": {
            "model": "general",
            "audioFormat": {
                "rawAudio": {
                    "audioEncoding": "LINEAR16_PCM",
                    "sampleRateHertz": f"{sample_rate}",
                    "audioChannelCount": "1",
                }
            },
            "textNormalization": {
                "textNormalization": "TEXT_NORMALIZATION_ENABLED",
                "profanityFilter": False,
            },
            "languageRestriction": {
                "restrictionType": "WHITELIST",
                "languageCode": ["ru-RU"]
            },
        },
        "recognitionClassifier": {
            "classifiers": [{"classifier": "INTENT", "triggers": ["ON_UTTERANCE"]}]
        },
        "speakerLabeling": {"speakerLabeling": "SPEAKER_LABELING_ENABLED"},
    }
    async with aiohttp.ClientSession(base_url=BASE_URL) as session, session.post(
        url="/stt/v3/recognizeFileAsync", headers=headers, json=payload
    ) as response:
        response.raise_for_status()
        return await response.json()


async def get_operation(operation_id: str) -> dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {settings.yandexcloud.api_key}",
    }
    async with aiohttp.ClientSession(base_url=BASE_URL) as session, session.get(
        url=f"/operations/{operation_id}", headers=headers
    ) as response:
        response.raise_for_status()
        return await response.json()


async def get_recognition(operation_id: str) -> dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {settings.yandexcloud.api_key}"
    }
    async with aiohttp.ClientSession(base_url=BASE_URL) as session, session.get(
        url="/stt/v3/getRecognition", headers=headers, params={"operationId": operation_id}
    ) as response:
        response.raise_for_status()
        return await response.json()


async def recognize_async(
        wav_file: bytes,
        sample_rate: Literal[8000, 16000, 48000] = 16000,
        poll_interval: int = 5,
        max_wait_time: int = 300
):
    operation = await create_recognition_task(wav_file, sample_rate)
    start_time = time.time()
    while time.time() - start_time <= max_wait_time or not operation["done"]:
        await asyncio.sleep(poll_interval)
        operation = await get_operation(operation["id"])
    if not operation["done"]:
        return "..."
    recognition = await get_recognition(operation["id"])
    return recognition
