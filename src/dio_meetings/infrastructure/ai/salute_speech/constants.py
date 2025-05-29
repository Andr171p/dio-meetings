from typing import Literal


# Salute-Speech базовый URL:
SALUTE_SPEECH_URL = "https://smartspeech.sber.ru/rest/v1"

# Sberbank-devices URL:
SBER_DEVICES_URL = "https://ngw.devices.sberbank.ru:9443/api/v2"

# Доступные значения Scope:
AVAILABLE_SCOPES = Literal[
    "SALUTE_SPEECH_PERS",
    "SALUTE_SPEECH_CORP"
]

# Допустимые Content-Type файлов:
AVAILABLE_CONTENT_TYPES = Literal[
    "audio/mpeg",
    "audio/ogg;codecs=opus"
]

# Допустимые модели Yandex-Speech:
AVAILABLE_MODELS = Literal[
    "general",
    "callcenter"
]

# Допустимые форматы аудио:
AVAILABLE_AUDIO_ENCODINGS = Literal[
    "PCM_S16LE",  # PCM signed 16bit little-endian, с заголовком WAV или без.
    # Частота дискретизации – от 8 до 96 кГц. Если без заголовка, то параметр sample_rate – обязательный.
    # Максимальное количество каналов – 8.
    # Значение Content-Type – audio/x-pcm;bit=16;rate=XXX.
    "OPUS",  # Opus в контейнере ogg.
    # Параметр sample_rate – необязательный.
    # Поддерживается только одноканальный звук.
    # Значение Content-Type – audio/ogg;codecs=opus.
    "MP3",  # MP3
    # Параметр sample_rate – необязательный.
    # Максимальное количество каналов – 2.
    # Значение Content-Type – audio/mpeg.
    "FLAC",  # FLAC
    # Параметр sample_rate – необязательный.
    # Максимальное количество каналов – 8.
    # Значение Content-Type – audio/flac.
    "ALAW",  # G.711 A-law, с заголовком WAV или без.
    # Частота дискретизации – от 8 до 96 кГц. Если без заголовка, то параметр sample_rate – обязательный.
    # Максимальное количество каналов – 8.
    # Значение Content-Type – audio/pcma;rate=XXX.
    "MULAW",  # G.711 μ-law, с заголовком WAV или без.
    # Частота дискретизации – от 8 до 96 кГц. Если без заголовка, то параметр sample_rate – обязательный.
    # Максимальное количество каналов – 8.
    # Значение Content-Type – audio/pcmu;rate=XXX.
]

# Поддерживаемые языки:
SUPPORTED_LANGUAGES = Literal[
    "ru-RU",  # Русский
    "en-US",  # Английский
    "kk-KZ"  # Казахский
]

# Статус коды:
STATUS_200_OK = 200
STATUS_401_UNAUTHORIZED = 401


# Настройки распознавания речи:
HYPOTHESES_COUNT = 1  # Количество сообщаемых альтернативных гипотез распознанной речи.
NO_SPEECH_TIMEOUT = 7  # Интервал ожидания речи пользователя.
MAX_SPEECH_TIMEOUT = 20  # Определение максимальной длины высказывания до форсированного EOU. По умолчанию стоит 20 секунд.
WORDS = []  # Слова распознавание которых хотим усилить
ENABLE_LETTERS = False  # Модель коротких фраз, улучшающая распознавание отдельных букв и коротких слов.
# Используется только в паре с WORDS
EOU_TIMEOUT = 1  # Настройка распознавания конца фразы (End of Utterance - eou).
# Такое распознавание будет ожидаться после конца фразы столько секунд, сколько установлено в этом параметре.
# По умолчанию распознавание конца фразы срабатывает после 1 секунды
# Используется в паре с WORDS


# Таймаут для получения статуса задачи:
DEFAULT_ASYNC_TIMEOUT = 1