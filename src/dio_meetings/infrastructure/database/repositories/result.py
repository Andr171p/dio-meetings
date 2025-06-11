from typing import Optional

import logging
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import ResultOrm

from src.dio_meetings.core.domain import Result
from src.dio_meetings.core.dto import CreatedResult
from src.dio_meetings.core.base import ResultRepository
from src.dio_meetings.core.exceptions import CreateDataError, ReadDataError, DeleteDataError


class SQLResultRepository(ResultRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = session

    async def create(self, result: Result) -> CreatedResult:
        try:
            stmt = (
                insert(ResultOrm)
                .values(**result.model_dump())
                .returning(ResultOrm)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            created_result = result.scalar_one()
            return CreatedResult.model_validate(created_result)
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while creating result: {e}")
            raise CreateDataError(f"Error while creating result: {e}") from e

    async def read(self, result_id: UUID) -> Optional[CreatedResult]:
        try:
            stmt = (
                select(ResultOrm)
                .where(ResultOrm.result_id == result_id)
            )
            result = await self.session.execute(stmt)
            created_result = result.scalar_one_or_none()
            return CreatedResult.model_validate(created_result) if created_result else None
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while reading result: {e}")
            raise ReadDataError(f"Error while reading result: {e}") from e

    async def delete(self, result_id: UUID) -> bool:
        try:
            stmt = (
                delete(ResultOrm)
                .where(ResultOrm.result_id == result_id)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount() > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while deleting result: {e}")
            raise DeleteDataError(f"Error while deleting result: {e}") from e
