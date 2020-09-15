import shutil
import sys
from pathlib import Path

import pytest

from pandas_profiling.model.summarizer import PandasProfilingSummarizer
from pandas_profiling.model.typeset import ProfilingTypeSet
from pandas_profiling.utils.cache import cache_file


def pytest_configure(config):
    config.addinivalue_line("markers", "linux: Test with linux")
    config.addinivalue_line("markers", "win32: Test with windows")
    config.addinivalue_line("markers", "darwin: Test with darwin")

    plugin = config.pluginmanager.getplugin("mypy")
    plugin.mypy_argv.append("--ignore-missing-imports")


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


@pytest.fixture(scope="module")
def summarizer(typeset):
    return PandasProfilingSummarizer(typeset)


@pytest.fixture(scope="module")
def typeset():
    return ProfilingTypeSet()


def pytest_runtest_setup(item):
    platforms = {"darwin", "linux", "win32"}
    supported_platforms = platforms.intersection(
        mark.name for mark in item.iter_markers()
    )
    plat = sys.platform
    if supported_platforms and plat not in supported_platforms:
        pytest.skip("cannot run on platform {}".format(plat))
