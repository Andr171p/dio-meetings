from dishka import Provider, provide, Scope, from_context, make_async_container

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from faststream.redis import RedisBroker

from .core.use_cases import ProtocolComposer
from .core.base import STTService, LLMService, DocumentBuilder, FileRepository, TaskRepository

from .infrastructure.documents.word import DOCXBuilder
from .infrastructure.llms.yandex_gpt import YandexGPTService
from .infrastructure.stt.salute_speech import SaluteSpeechService
from .infrastructure.s3.repository import S3Repository
from .infrastructure.database.session import create_session_maker
from .infrastructure.database.repository import SQLTaskRepository

from .settings import Settings


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_broker(self, config: Settings) -> RedisBroker:
        return RedisBroker(config.redis.redis_url)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Settings) -> async_sessionmaker[AsyncSession]:
        return create_session_maker(config.postgres)

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
    def get_document_builder(self) -> DocumentBuilder:
        return DOCXBuilder()

    @provide(scope=Scope.APP)
    def get_meeting_protocol_composer(
            self,
            stt_service: STTService,
            llm_service: LLMService,
            document_builder: DocumentBuilder
    ) -> ProtocolComposer:
        return ProtocolComposer(
            stt_service=stt_service,
            llm_service=llm_service,
            document_builder=document_builder
        )

    @provide(scope=Scope.APP)
    def get_file_repository(self, config: Settings) -> FileRepository:
        return S3Repository(
            url=config.minio.MINIO_URL,
            access_key=config.minio.MINIO_USER,
            secret_key=config.minio.MINIO_PASSWORD
        )

    @provide(scope=Scope.APP)
    def get_task_repository(self, session_factory: async_sessionmaker[AsyncSession]) -> TaskRepository:
        return SQLTaskRepository(session_factory)


settings = Settings()

container = make_async_container(AppProvider(), context={Settings: settings})
