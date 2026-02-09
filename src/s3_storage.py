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
async def _get_s3_client():
    async with session.create_client(**config) as s3_client:
        yield s3_client


async def upload(file: bytes, key: str) -> None:
    async with _get_s3_client() as s3_client:
        await s3_client.put_object(Bucket=BUCKET_NAME, Key=key, Body=file)


async def download(key: str) -> bytes:
    async with _get_s3_client() as s3_client:
        response = await s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
        return await response["Body"].read()


async def delete(key: str) -> None:
    async with _get_s3_client() as s3_client:
        await s3_client.delete_object(Bucket=BUCKET_NAME, Key=key)


async def create_presigned_url(key: str, expires_in: int = 60 * 60) -> str:
    async with _get_s3_client() as s3_client:
        return await s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=expires_in
        )
