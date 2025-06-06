from typing import Any, Union
from collections.abc import AsyncGenerator

import io
import logging
from uuid import UUID

from aiobotocore.session import get_session
from aiobotocore.client import AioBaseClient
from aiobotocore.config import AioConfig

from .exceptions import S3Error

from src.dio_meetings.core.base import FileRepository


SERVICE_NAME = "s3"


class S3Repository(FileRepository):
    def __init__(
            self,
            url: str,
            access_key: str,
            secret_key: str,
            secure: bool = False
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._params = {
            "endpoint_url": url,
            "aws_access_key": access_key,
            "aws_secret_access_key": secret_key,
            "use_ssl": secure
        }
        self._config = AioConfig(
            region_name="us-east-1",
            s3={"addressing_style": "path"}
        )

    async def _get_client(self) -> AsyncGenerator[AioBaseClient, Any]:
        session = get_session()
        async with session.create_client(**self._params) as client:
            yield client

    async def create_bucket(self, bucket_name: str) -> None:
        try:
            async with self._get_client() as client:
                await client.create_bucket(Bucket=bucket_name)
            self._logger.info(f"Bucket {bucket_name} created successfully")
        except Exception as e:
            self._logger.error(f"Error while creating bucket: {e}")
            raise S3Error(f"Error while creating bucket: {e}") from e

    async def upload_file(
            self,
            file: Union[io.BytesIO, bytes],
            file_name: Union[str, UUID],
            bucket_name: str,
    ) -> None:
        try:
            async with self._get_client() as client:
                await client.put_object(
                    Bucket=bucket_name,
                    Key=str(file_name),
                    Body=file
                )
        except Exception as e:
            raise S3Error(f"Error while uploading file: {e}") from e

    async def download_file(self, file_name: Union[UUID, str], bucket_name: str) -> ...:
        try:
            async with self._get_client() as client:
                response = await client.get_object(Bucket=bucket_name, Key=str(file_name))
            return response["Body"]
        except Exception as e:
            self._logger.error(f"Error while receiving file: {e}")
            raise S3Error(f"Error while receiving file: {e}") from e

    async def delete_file(self, file_name: Union[UUID, str], bucket_name: str) -> str:
        try:
            async with self._get_client() as client:
                await client.delete_object(Bucket=bucket_name, Key=str(file_name))
            return file_name
        except Exception as e:
            self._logger.error(f"Error while deleting file: {e}")
            raise S3Error(f"Error while deleting file: {e}") from e
