from dishka import Provider, provide, Scope, from_context, make_async_container

from .core.use_cases import MeetingProtocolComposer
from .core.base import STTService, LLMService, DocumentBuilder, FileRepository

from .infrastructure.documents.word import DOCXBuilder
from .infrastructure.llms.yandex_gpt import YandexGPTService
from .infrastructure.stt.salute_speech import SaluteSpeechService
from .infrastructure.s3.repository import S3Repository

from .settings import Settings


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

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
    ) -> MeetingProtocolComposer:
        return MeetingProtocolComposer(
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


settings = Settings()

container = make_async_container(AppProvider(), context={Settings: settings})
