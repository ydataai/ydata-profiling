"""Dataset cache utility functions"""
import zipfile
from pathlib import Path
from urllib import request

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

    file_path = data_path / file_name

    # If not exists, download and create file
    if not file_path.exists():
        response = request.urlopen(url)
        file_path.write_bytes(response.read())

    return file_path


def cache_zipped_file(file_name: str, url: str) -> Path:
    """Check if file_name already is in the data path, otherwise download it from url.

    Args:
        file_name: the file name
        url: the URL of the dataset

    Returns:
        The relative path to the dataset
    """

    data_path = get_data_path()
    data_path.mkdir(exist_ok=True)

    file_path = data_path / file_name

    # If not exists, download and create file
    if not file_path.exists():
        response = request.urlopen(url)

        tmp_path = data_path / "tmp.zip"
        tmp_path.write_bytes(response.read())

        with zipfile.ZipFile(tmp_path, "r") as zip_file:
            zip_file.extract(file_path.name, data_path)

        tmp_path.unlink()

    return file_path
