from typing import Optional

from uuid import UUID

from sqlalchemy import insert, select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import FileMetadataOrm

from src.dio_meetings.core.domain import FileMetadata
from src.dio_meetings.core.base import FileMetadataRepository
from src.dio_meetings.core.exceptions import CreationError, ReadingError, DeletingError


class SQLFileMetadataRepository(FileMetadataRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, file_metadata: FileMetadata) -> FileMetadata:
        try:
            stmt = (
                insert(FileMetadataOrm)
                .values(**file_metadata.model_dump(exclude_none=True))
                .returning(FileMetadataOrm)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            created_file_metadata = result.scalar_one()
            return FileMetadata.model_validate(created_file_metadata)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise CreationError(f"Error while creating meeting: {e}") from e

    async def read(self, id: UUID) -> Optional[FileMetadata]:
        try:
            stmt = (
                select(FileMetadataOrm)
                .where(FileMetadataOrm.id == id)
            )
            result = await self.session.execute(stmt)
            file_metadata = result.scalar_one_or_none()
            return FileMetadata.model_validate(file_metadata) if file_metadata else None
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ReadingError(f"Error while reading meeting: {e}") from e

    async def read_all(self, bucket: Optional[str] = None) -> list[FileMetadata]:
        try:
            stmt = select(FileMetadataOrm)
            if bucket:
                stmt = stmt.where(FileMetadataOrm.bucket == bucket)
            results = await self.session.execute(stmt)
            files_metadata = results.scalars().all()
            return [FileMetadata.model_validate(files_metadata) for files_metadata in files_metadata]
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ReadingError(f"Error while reading meetings: {e}") from e

    async def delete(self, id: UUID) -> bool:
        try:
            stmt = (
                delete(FileMetadataOrm)
                .where(FileMetadataOrm.id == id)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DeletingError(f"Error while deleting meeting: {e}") from e
