from typing import Optional

import logging
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import MeetingOrm, TaskOrm

from src.dio_meetings.core.domain import Meeting
from src.dio_meetings.core.base import MeetingRepository
from src.dio_meetings.core.dto import CreatedMeeting, CreatedResult
from src.dio_meetings.core.exceptions import CreationError, ReadingError, DeletingError


class SQLMeetingRepository(MeetingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = session

    async def create(self, meeting: Meeting) -> CreatedMeeting:
        try:
            stmt = (
                insert(MeetingOrm)
                .values(**meeting.model_dump())
                .returning(MeetingOrm)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            created_meeting = result.scalar_one()
            return CreatedMeeting.model_validate(created_meeting)
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while creating meeting: {e}")
            raise CreationError(f"Error while creating meeting: {e}") from e

    async def read(self, meeting_id: UUID) -> Optional[CreatedMeeting]:
        try:
            stmt = (
                select(MeetingOrm)
                .where(MeetingOrm.meeting_id == meeting_id)
            )
            result = await self.session.execute(stmt)
            created_meeting = result.scalar_one_or_none()
            return CreatedMeeting.model_validate(created_meeting) if created_meeting else None
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while reading meeting: {e}")
            raise ReadingError(f"Error while reading meeting: {e}") from e

    async def read_all(self) -> list[CreatedMeeting]:
        try:
            stmt = select(MeetingOrm)
            results = await self.session.execute(stmt)
            created_meetings = results.scalars().all()
            return [
                CreatedMeeting.model_validate(created_meeting)
                for created_meeting in created_meetings
            ] if created_meetings else []
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while reading meetings: {e}")
            raise ReadingError(f"Error while reading meetings: {e}") from e

    async def delete(self, meeting_id: UUID) -> bool:
        try:
            stmt = (
                delete(MeetingOrm)
                .where(MeetingOrm.meeting_id == meeting_id)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount() > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while deleting meeting: {e}")
            raise DeletingError(f"Error while deleting meeting: {e}") from e

    async def get_result(self, meeting_id: UUID) -> Optional[CreatedResult]:
        try:
            stmt = (
                select(TaskOrm.result)
                .where(
                    TaskOrm.meeting_id == meeting_id,
                    TaskOrm.status == "DONE"
                )
            )
            result = await self.session.execute(stmt)
            created_result = result.scalar_one_or_none()
            return CreatedResult.model_validate(created_result) if created_result else None
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(f"Error while receiving result: {e}")
            raise ReadingError(f"Error while receiving result: {e}") from e
