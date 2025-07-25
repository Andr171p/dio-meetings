from typing import Any
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import logging

from aiobotocore.session import get_session
from aiobotocore.client import AioBaseClient

from ..core.base import FileStorage
from ..core.exceptions import FileStoreError, UploadingError, DownloadingError


SERVICE_NAME = "s3"


class S3Client(FileStorage):
    def __init__(
            self,
            url: str,
            access_key: str,
            secret_key: str,
            secure: bool = False
    ) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = {
            "endpoint_url": url,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "use_ssl": secure,
            "region_name": "us-east-1",
            "service_name": "s3"
        }
        self.session = get_session()

    @asynccontextmanager
    async def _get_client(self) -> AsyncGenerator[AioBaseClient, Any]:
        async with self.session.create_client(**self.config) as client:
            yield client

    async def create_bucket(self, bucket_name: str) -> None:
        try:
            async with self._get_client() as client:
                await client.create_bucket(Bucket=bucket_name)
            self.logger.info(f"Bucket {bucket_name} created successfully")
        except Exception as e:
            self.logger.error(f"Error while creating bucket: {e}")
            raise FileStoreError(f"Error while creating bucket: {e}") from e

    async def upload_file(self, data: bytes, key: str, bucket: str) -> None:
        try:
            async with self._get_client() as client:
                await client.put_object(Bucket=bucket, Key=key, Body=data)
        except Exception as e:
            raise UploadingError(f"Error while uploading file: {e}") from e

    async def download_file(self, key: str, bucket: str) -> bytes:
        try:
            async with self._get_client() as client:
                response = await client.get_object(Bucket=bucket, Key=key)
                body = response["Body"]
                return await body.read()
        except Exception as e:
            self.logger.error(f"Error while receiving file: {e}")
            raise DownloadingError(f"Error while receiving file: {e}") from e

    async def remove_file(self, key: str, bucket: str) -> str:
        try:
            async with self._get_client() as client:
                await client.delete_object(Bucket=bucket, Key=key)
            return key
        except Exception as e:
            self.logger.error(f"Error while deleting file: {e}")
            raise FileStoreError(f"Error while deleting file: {e}") from e
