from pathlib import Path

import pytest

from pandas_profiling.utils.dataframe import read_pandas


def test_read_pandas_parquet():
    p = Path('dataframe.parquet')
    with pytest.raises(OSError) as e:
        read_pandas(p)

    assert str(e.value) == 'Passed non-file path: dataframe.parquet'


def test_read_pandas_csv():
    p = Path('dataframe.csv')
    with pytest.raises(OSError) as e:
        read_pandas(p)

    assert str(e.value) == "[Errno 2] File b'dataframe.csv' does not exist: b'dataframe.csv'"


def test_read_pandas_json():
    p = Path('dataframe.json')
    with pytest.raises(ValueError) as e:
        read_pandas(p)

    assert str(e.value) == "Expected object or value"

