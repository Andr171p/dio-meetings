from typing import Literal


# Salute Speech базовый URL:
SALUTE_SPEECH_URL = "https://smartspeech.sber.ru/rest/v1/"

# Sberbank-devices URL:
SBER_DEVICES_URL = "https://ngw.devices.sberbank.ru:9443/api/v2"

# Доступные значения Scope:
AVAILABLE_SCOPES = Literal[
    "SALUTE_SPEECH_PERS",
    "SALUTE_SPEECH_CORP"
]

# Статус коды:
STATUS_200_OK = 200
STATUS_401_UNAUTHORIZED = 401
