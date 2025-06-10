from .constants import CONTENT_TYPE, AUDIO_ENCODING


CONTENT_TYPES_DICT: dict[str, CONTENT_TYPE] = {
    "mp3": "audio/mpeg",
    "ogg": "audio/ogg;codecs=opus"
}

AUDIO_ENCODING_DICT: dict[str,AUDIO_ENCODING] = {
    "pcm": "PCM_S16LE",
    "ogg": "OPUS",
    "mp3": "MP3",
    "fcal": "FLAC"
}


def get_content_type(file_format: str) -> CONTENT_TYPE:
    content_type = CONTENT_TYPES_DICT.get(file_format)
    if not content_type:
        raise ValueError("Unsupported file type")
    return content_type


def get_audio_encoding(file_format: str) -> AUDIO_ENCODING:
    audio_encoding = AUDIO_ENCODING_DICT.get(file_format)
    if not audio_encoding:
        raise ValueError("Unsupported file type")
    return audio_encoding
