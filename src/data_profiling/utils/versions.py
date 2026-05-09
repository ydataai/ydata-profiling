# `importlib.metadata.version` is in the stdlib since Python 3.8.
# pyproject.toml pins `requires-python = ">=3.10,<3.14"`, so the previous
# `pkg_resources` fallback was dead code under any supported runtime.
# Removing it also drops a runtime dependency on setuptools, which now
# raises `ModuleNotFoundError: No module named 'pkg_resources'` on
# setuptools >= 81 where pkg_resources was removed.
from importlib.metadata import version


def pandas_version() -> list:
    return list(map(int, version("pandas").split(".")))


def pandas_major_version() -> int:
    return pandas_version()[0]


def is_pandas_1() -> bool:
    return pandas_major_version() == 1
