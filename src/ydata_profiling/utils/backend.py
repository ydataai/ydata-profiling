"""
Backend detection utilities for pandas and spark.
"""
import importlib


def is_pyspark_installed() -> bool:
    """Check if PySpark is installed without importing it."""
    return importlib.util.find_spec("pyspark") is not None
