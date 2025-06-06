from typing import Any
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import logging

from aiobotocore.session import get_session
from aiobotocore.client import AioBaseClient

from .exceptions import S3Error
from ...core.base import FileRepository


SERVICE_NAME = "s3"


class S3Repository(FileRepository):
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
            "aws_access_key": access_key,
            "aws_secret_access_key": secret_key,
            "use_ssl": secure
        }
        self.session = get_session()

    @asynccontextmanager
    async def _get_client(self) -> AsyncGenerator[AioBaseClient, Any]:
        async with self.session.create_client(SERVICE_NAME, **self.config) as client:
            yield client

    async def create_bucket(self, bucket_name: str) -> None:
        try:
            async with self._get_client() as client:
                await client.create_bucket(Bucket=bucket_name)
            self.logger.info(f"Bucket {bucket_name} created successfully")
        except Exception as e:
            self.logger.error(f"Error while creating bucket: {e}")
            raise S3Error(f"Error while creating bucket: {e}") from e

    async def upload_file(
            self,
            file_data: bytes,
            file_name: str,
            bucket_name: str,
    ) -> None:
        try:
            async with self._get_client() as client:
                await client.put_object(
                    Bucket=bucket_name,
                    Key=file_name,
                    Body=file_data
                )
        except Exception as e:
            raise S3Error(f"Error while uploading file: {e}") from e

    async def download_file(self, file_name: str, bucket_name: str) -> bytes:
        try:
            async with self._get_client() as client:
                response = await client.get_object(Bucket=bucket_name, Key=file_name)
            return response["Body"]
        except Exception as e:
            self.logger.error(f"Error while receiving file: {e}")
            raise S3Error(f"Error while receiving file: {e}") from e

    async def delete_file(self, file_name: str, bucket_name: str) -> str:
        try:
            async with self._get_client() as client:
                await client.delete_object(Bucket=bucket_name, Key=file_name)
            return file_name
        except Exception as e:
            self.logger.error(f"Error while deleting file: {e}")
            raise S3Error(f"Error while deleting file: {e}") from e
