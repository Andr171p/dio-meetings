import logging
import math
from collections.abc import AsyncIterable
from contextlib import asynccontextmanager

from aiobotocore.session import get_session

from .settings import settings

BASE_URL = "https://storage.yandexcloud.net/"
BUCKET_NAME = "dev-uploads-data"

logger = logging.getLogger(__name__)

session = get_session()
config = {
    "service_name": "s3",
    "endpoint_url": BASE_URL,
    "aws_access_key_id": settings.yandexcloud.access_key_id,
    "aws_secret_access_key": settings.yandexcloud.secret_access_key,
}


@asynccontextmanager
async def _get_client():
    async with session.create_client(**config) as client:
        yield client


async def upload(content: bytes, key: str) -> None:
    async with _get_client() as client:
        await client.put_object(Bucket=BUCKET_NAME, Key=key, Body=content)


async def upload_multipart(chunks: AsyncIterable[bytes], key: str) -> None:
    upload_id = None
    parts = []
    async with _get_client() as client:
        part_number = 1
        async for chunk in chunks:
            if upload_id is None:
                response = await client.create_multipart_upload(Bucket=BUCKET_NAME, Key=key)
                upload_id = response["UploadId"]
                logger.info("Initiate multipart uploading, key - `%s`", key)
            response = await client.upload_part(
                Bucket=BUCKET_NAME,
                Key=key,
                UploadId=upload_id,
                PartNumber=part_number,
                Body=chunk,
            )
            parts.append({"PartNumber": part_number, "ETag": response["ETag"]})
            logger.info("Successful upload %s part for key `%s`", part_number, key)
            part_number += 1
        await client.complete_multipart_upload(
            Bucket=BUCKET_NAME,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )
        logger.info("Multipart upload completed %s parts for key `%s`", len(parts), key)


async def download(key: str) -> bytes:
    async with _get_client() as client:
        response = await client.get_object(Bucket=BUCKET_NAME, Key=key)
        return await response["Body"].read()


async def download_multipart(key: str, chunk_size: int = 1024 * 1024) -> AsyncIterable[bytes]:
    async with _get_client() as client:
        head = await client.head_object(Bucket=BUCKET_NAME, Key=key)
        size = head["ContentLength"]
        part_numbers = math.ceil(size / chunk_size)
        logger.info(
            "Start multipart downloading for key `%s`, size %s mb, total parts %s",
            key, round(size / (1024 * 1024), 2), part_numbers
        )
        for part_number in range(part_numbers):
            start = part_number * chunk_size
            end = min((part_number + 1) * chunk_size - 1, size - 1)
            logger.info("Downloading `%s` part %s : bytes %s-%s", key, part_number, start, end)
            response = await client.get_object(
                Bucket=BUCKET_NAME, Key=key, Range=f"bytes={start}-{end}"
            )
            content = await response["Body"].read()
            yield content


async def delete(key: str) -> None:
    async with _get_client() as client:
        await client.delete_object(Bucket=BUCKET_NAME, Key=key)


async def create_presigned_url(key: str, expires_in: int = 60 * 60) -> str:
    async with _get_client() as client:
        return await client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=expires_in
        )
