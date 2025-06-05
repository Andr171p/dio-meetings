from typing import Union

from pathlib import Path


def get_file_extension(file_path: Union[Path, str]) -> str:
    return file_path.split(".")[-1]

