import sys

try:
    from importlib.metadata import version
except ImportError:
    import pkg_resources

    version = lambda x: pkg_resources.get_distribution(x).version


def pandas_version() -> list:
    return map(int, version("pandas").split("."))


def pandas_major_version() -> int:
    return pandas_version()[0]


def is_pandas_1() -> bool:
    return pandas_major_version == 1
