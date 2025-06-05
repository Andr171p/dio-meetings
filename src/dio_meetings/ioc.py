from dishka import Provider, provide, Scope, from_context, make_container

from .core.base import STTService, LLMService
from .core.use_cases import MeetingProtocolComposer

from .infrastructure.llms.yandex_gpt import YandexGPTService
from .infrastructure.stt.salute_speech import SaluteSpeechService

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
    def get_meeting_protocol_composer(
            self,
            stt_service: STTService,
            llm_service: LLMService
    ) -> MeetingProtocolComposer:
        return MeetingProtocolComposer(
            stt_service=stt_service,
            llm_service=llm_service
        )


settings = Settings()

container = make_container(AppProvider(), context={Settings: settings})
