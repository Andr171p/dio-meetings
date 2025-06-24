from collections.abc import AsyncIterable

from dishka import Provider, provide, Scope, from_context, make_async_container

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from faststream.redis import RedisBroker

from .core.services import SummarizationService, TaskService, FileService
from .core.base import (
    BaseLLM,
    BaseSTT,
    DocumentFactory,
    FileStorage,
    TaskRepository,
    FileMetadataRepository
)

from .infrastructure.documents import MicrosoftWordFactory
from .infrastructure.llms.yandex_gpt import YandexGPT
from .infrastructure.stt.salute_speech import SaluteSpeech
from src.dio_meetings.infrastructure.s3 import S3Client
from .infrastructure.database.session import create_session_maker
from src.dio_meetings.infrastructure.database.repositories import (
    SQLTaskRepository,
    SQLFileMetadataRepository
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
    def get_stt(self, config: Settings) -> BaseSTT:
        return SaluteSpeech(
            api_key=config.salute_speech.API_KEY,
            scope=config.salute_speech.SCOPE
        )

    @provide(scope=Scope.APP)
    def get_llm(self, config: Settings) -> BaseLLM:
        return YandexGPT(
            folder_id=config.yandex_gpt.FOLDER_ID,
            api_key=config.yandex_gpt.API_KEY
        )

    @provide(scope=Scope.APP)
    def get_document_factory(self) -> DocumentFactory:
        return MicrosoftWordFactory()

    @provide(scope=Scope.APP)
    def get_file_storage(self, config: Settings) -> FileStorage:
        return S3Client(
            url=config.minio.MINIO_URL,
            access_key=config.minio.MINIO_USER,
            secret_key=config.minio.MINIO_PASSWORD
        )

    @provide(scope=Scope.REQUEST)
    def get_task_repository(self, session: AsyncSession) -> TaskRepository:
        return SQLTaskRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_file_metadata_repository(self, session: AsyncSession) -> FileMetadataRepository:
        return SQLFileMetadataRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_task_service(
            self,
            task_repository: TaskRepository,
            file_metadata_repository: FileMetadataRepository,
            file_storage: FileStorage,
            broker: RedisBroker
    ) -> TaskService:
        return TaskService(
            task_repository=task_repository,
            file_metadata_repository=file_metadata_repository,
            file_storage=file_storage,
            broker=broker
        )

    @provide(scope=Scope.APP)
    def get_summarization_service(
            self,
            stt: BaseSTT,
            llm: BaseLLM,
            document_factory: DocumentFactory
    ) -> SummarizationService:
        return SummarizationService(
            stt=stt,
            llm=llm,
            document_factory=document_factory
        )

    @provide(scope=Scope.REQUEST)
    def get_file_service(
            self,
            file_metadata_repository: FileMetadataRepository,
            file_storage: FileStorage
    ) -> FileService:
        return FileService(
            file_metadata_repository=file_metadata_repository,
            file_storage=file_storage
        )


settings = Settings()

container = make_async_container(AppProvider(), context={Settings: settings})
