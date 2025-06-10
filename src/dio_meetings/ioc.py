from collections.abc import AsyncIterable

from dishka import Provider, provide, Scope, from_context, make_async_container

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from faststream.redis import RedisBroker

from .core.services import SummarizationService, TaskService, MeetingService
from .core.base import (
    STTService,
    LLMService,
    DocumentFactory,
    S3Repository,
    MeetingRepository,
    TaskRepository,
    ResultRepository
)

from .infrastructure.documents import MicrosoftWordFactory
from .infrastructure.llms.yandex_gpt import YandexGPTService
from .infrastructure.stt.salute_speech import SaluteSpeechService
from .infrastructure.s3.repository import MinioS3Repository
from .infrastructure.database.session import create_session_maker
from src.dio_meetings.infrastructure.database.repositories import (
    SQLTaskRepository,
    SQLMeetingRepository,
    SQLResultRepository
)

from .settings import Settings


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_broker(self, config: Settings) -> RedisBroker:
        return RedisBroker(config.redis.redis_url)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Settings) -> async_sessionmaker[AsyncSession]:
        return create_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_stt_service(self, config: Settings) -> STTService:
        return SaluteSpeechService(
            api_key=config.salute_speech.API_KEY,
            scope=config.salute_speech.SCOPE
        )

    @provide(scope=Scope.APP)
    def get_llm_service(self, config: Settings) -> LLMService:
        return YandexGPTService(
            folder_id=config.yandex_gpt.FOLDER_ID,
            api_key=config.yandex_gpt.API_KEY
        )

    @provide(scope=Scope.APP)
    def get_document_factory(self) -> DocumentFactory:
        return MicrosoftWordFactory()

    @provide(scope=Scope.APP)
    def get_s3_repository(self, config: Settings) -> S3Repository:
        return MinioS3Repository(
            url=config.minio.MINIO_URL,
            access_key=config.minio.MINIO_USER,
            secret_key=config.minio.MINIO_PASSWORD
        )

    @provide(scope=Scope.REQUEST)
    def get_meeting_repository(self, session: AsyncSession) -> MeetingRepository:
        return SQLMeetingRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_task_repository(self, session: AsyncSession) -> TaskRepository:
        return SQLTaskRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_result_repository(self, session: AsyncSession) -> ResultRepository:
        return SQLResultRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_meeting_service(
            self,
            meetings_repository: MeetingRepository,
            s3_repository: S3Repository
    ) -> MeetingService:
        return MeetingService(
            meeting_repository=meetings_repository,
            s3_repository=s3_repository
        )

    @provide(scope=Scope.REQUEST)
    def get_task_service(
            self,
            task_repository: TaskRepository,
            result_repository: ResultRepository,
            s3_repository: S3Repository,
            broker: RedisBroker
    ) -> TaskService:
        return TaskService(
            task_repository=task_repository,
            result_repository=result_repository,
            s3_repository=s3_repository,
            broker=broker
        )

    @provide(scope=Scope.APP)
    def get_summarization_service(
            self,
            stt_service: STTService,
            llm_service: LLMService,
            document_factory: DocumentFactory
    ) -> SummarizationService:
        return SummarizationService(
            stt_service=stt_service,
            llm_service=llm_service,
            document_factory=document_factory
        )


settings = Settings()

container = make_async_container(AppProvider(), context={Settings: settings})
