"""Dataset cache utility functions"""
from pathlib import Path

import requests

from pandas_profiling.utils.paths import get_data_path


def cache_file(file_name: str, url: str) -> Path:
    """Check if file_name already is in the data path, otherwise download it from url.

    Args:
        file_name: the file name
        url: the URL of the dataset

    Returns:
        The relative path to the dataset
    """

    data_path = get_data_path()
    data_path.mkdir(exist_ok=True)

    # If not exists, download and create file
    if not (data_path / file_name).exists():
        data = requests.get(url)
        (data_path / file_name).write_bytes(data.content)

    return data_path / file_name
