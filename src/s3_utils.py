from contextlib import asynccontextmanager

from aiobotocore.session import get_session

from .settings import settings

BASE_URL = "https://storage.yandexcloud.net/"
BUCKET_NAME = "dev-uploads-data"

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


async def download(key: str) -> bytes:
    async with _get_client() as client:
        response = await client.get_object(Bucket=BUCKET_NAME, Key=key)
        return await response["Body"].read()


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
