"""Common util functions (e.g. missing in Python)."""
import collections
import warnings
import zipfile
from datetime import datetime, timedelta

# Monkeypatch bug in imagehdr
from imghdr import tests
from pathlib import Path
from typing import Mapping

VERSION_WARNING = """Warning : using pyspark 2.3/2.4 with pyarrow >= 0.15 
                        you might get errors with pyarrow's toPandas() functions because 
                        pyspark 2.3/2.4 is incompatible with pyarrow >= 0.15. You may need to set ARROW_PRE_0_15_IPC_FORMAT=1
                        in your spark.env to fix pyarrows errors if they occur.
                see https://spark.apache.org/docs/3.0.0-preview/sql-pyspark-pandas-with-arrow.html#compatibiliy-setting-for-pyarrow--0150-and-spark-23x-24x"""


def update(d: dict, u: Mapping) -> dict:
    """Recursively update a dict.

    Args:
        d: Dictionary to update.
        u: Dictionary with values to use.

    Returns:
        The merged dictionary.
    """
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def _copy(self, target):
    """Monkeypatch for pathlib

    Args:
        self:
        target:

    Returns:

    """
    import shutil

    assert self.is_file()
    shutil.copy(str(self), target)


Path.copy = _copy  # type: ignore


def extract_zip(outfile, effective_path):
    try:
        with zipfile.ZipFile(outfile) as z:
            z.extractall(effective_path)
    except zipfile.BadZipFile as e:
        raise ValueError("Bad zip file", e)


def test_jpeg1(h, f):
    """JPEG data in JFIF format"""
    if b"JFIF" in h[:23]:
        return "jpeg"


JPEG_MARK = (
    b"\xff\xd8\xff\xdb\x00C\x00\x08\x06\x06"
    b"\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f"
)


def test_jpeg2(h, f):
    """JPEG with small header"""
    if len(h) >= 32 and 67 == h[5] and h[:32] == JPEG_MARK:
        return "jpeg"


def test_jpeg3(h, f):
    """JPEG data in JFIF or Exif format"""
    if h[6:10] in (b"JFIF", b"Exif") or h[:2] == b"\xff\xd8":
        return "jpeg"


tests.append(test_jpeg1)
tests.append(test_jpeg2)
tests.append(test_jpeg3)


def convert_timestamp_to_datetime(timestamp: int) -> datetime:
    if timestamp >= 0:
        return datetime.fromtimestamp(timestamp)
    else:
        return datetime(1970, 1, 1) + timedelta(seconds=int(timestamp))


def test_for_pyspark_pyarrow_incompatibility():
    """
    This code checks if the env is using pyspark 2.3/2.4 with pyarrow >= 0.15, but has not set ARROW_PRE_0_15_IPC_FORMAT to 1
    This will cause all toPandas() functions to break. If the env fits the pattern above, this code raises an warning
    in warnings module in order to let the user know how to fix this problem

    """

    try:
        # check versions
        import os

        import pyarrow
        import pyspark

        # get spark version as a tuple
        spark_version = pyspark.__version__.split(".")

        # if spark version == 2.3 or 2.4
        if spark_version[0] == "2" and spark_version[1] in ["3", "4"]:

            pyarrow_version = pyarrow.__version__.split(".")

            # this checks if the env has an incompatible arrow version (not < 0.15)
            if not (pyarrow_version[0] == "0" and int(pyarrow_version[1]) < 15):
                # if os variable is not set, likely unhandled
                if "ARROW_PRE_0_15_IPC_FORMAT" not in os.environ:
                    warnings.warn(VERSION_WARNING)
                else:
                    # if variable is not set to 1, incompatibility error
                    if os.environ["ARROW_PRE_0_15_IPC_FORMAT"] != 1:
                        warnings.warn(VERSION_WARNING)
    except Exception as e:
        warnings.warn(
            f"test for pyspark 2.3,2.4 incompatibility with arrow >= 0.15 failed, Exception {str(e)} raised"
        )
