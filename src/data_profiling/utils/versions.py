try:
    from importlib.metadata import version
except ImportError:
    import pkg_resources

    def version(pkg: str) -> str:  # type: ignore
        return pkg_resources.get_distribution(pkg).version


def pandas_version() -> list:
    return list(map(int, version("pandas").split(".")))


def pandas_major_version() -> int:
    return pandas_version()[0]


def is_pandas_1() -> bool:
    return pandas_major_version() == 1
