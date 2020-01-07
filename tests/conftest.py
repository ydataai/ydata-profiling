import pytest

from pandas_profiling.config import Config, config


@pytest.fixture(scope="function", autouse=True)
def func_header():
    # Reset the config
    Config.config = None
    config = Config()
