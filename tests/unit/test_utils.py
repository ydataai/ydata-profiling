from pathlib import Path

import pytest
import pandas as pd

from pandas_profiling.utils.dataframe import read_pandas, warn_read, expand_mixed


def test_read_pandas_parquet():
    p = Path("dataframe.parquet")
    with pytest.raises(OSError) as e:
        read_pandas(p)

    assert str(e.value) in [
        # pyarrow
        "Passed non-file path: dataframe.parquet",
        # fastparquet
        "[Errno 2] No such file or directory: 'dataframe.parquet'",
    ]


def test_read_pandas_csv():
    p = Path("dataframe.csv")
    with pytest.raises(OSError) as e:
        read_pandas(p)

    assert (
        str(e.value)
        == "[Errno 2] File b'dataframe.csv' does not exist: b'dataframe.csv'"
    )


def test_read_pandas_json():
    p = Path("dataframe.json")
    with pytest.raises(ValueError) as e:
        read_pandas(p)

    assert str(e.value) == "Expected object or value"


def test_warning():
    with pytest.warns(UserWarning):
        warn_read("test")


def test_expand():
    df = pd.DataFrame(data=[{"name": "John", "age": 30}, {"name": "Alice", "age": 25}])
    expanded_df = expand_mixed(df)
    assert expanded_df.shape == (2, 2)
