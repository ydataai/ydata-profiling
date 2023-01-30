import shutil
import sys
from pathlib import Path

import pytest

from ydata_profiling.config import Settings
from ydata_profiling.model.summarizer import PandasProfilingSummarizer
from ydata_profiling.model.typeset import ProfilingTypeSet
from ydata_profiling.utils.cache import cache_file


def pytest_configure(config):
    config.addinivalue_line("markers", "linux: Test with linux")
    config.addinivalue_line("markers", "win32: Test with windows")
    config.addinivalue_line("markers", "darwin: Test with darwin")


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


@pytest.fixture(scope="function")
def summarizer(typeset):
    return PandasProfilingSummarizer(typeset)


@pytest.fixture(scope="function")
def config():
    return Settings()


@pytest.fixture(scope="function")
def typeset(config):
    return ProfilingTypeSet(config)


def pytest_runtest_setup(item):
    platforms = {"darwin", "linux", "win32"}
    supported_platforms = platforms.intersection(
        mark.name for mark in item.iter_markers()
    )
    plat = sys.platform
    if supported_platforms and plat not in supported_platforms:
        pytest.skip(f"cannot run on platform {plat}")
