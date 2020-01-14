import shutil
from pathlib import Path

import pytest

from pandas_profiling.utils.cache import cache_file


@pytest.fixture(scope="function")
def get_data_file(tmpdir):
    def getter(file_name, url):
        source_file = cache_file(file_name, url)
        # Move to temporary directory
        test_path = Path(str(tmpdir))
        shutil.copy(str(source_file), str(test_path / file_name))
        return str(test_path / file_name)

    return getter


@pytest.fixture(scope="module")
def test_output_dir(tmpdir_factory):
    test_path = Path(str(tmpdir_factory.mktemp("test")))
    yield test_path
    shutil.rmtree(str(test_path))
