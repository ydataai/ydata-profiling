"""
    File with a function to check the backend being used
"""
import importlib


def is_pyspark_installed() -> bool:
    """Check if PySpark is installed without importing it."""
    return importlib.util.find_spec("pyspark") is not None
