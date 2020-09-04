from pathlib import Path

import pandas as pd
import pytest

from pandas_profiling.utils.dataframe import expand_mixed, read_pandas, warn_read


def test_read_pandas_parquet():
    p = Path("dataframe.parquet")
    with pytest.raises(OSError) as e:
        read_pandas(p)

    assert str(e.value) in [
        # pyarrow
        "Passed non-file path: dataframe.parquet",
        # fastparquet
        "[Errno 2] No such file or directory: 'dataframe.parquet'",
        str(FileNotFoundError("dataframe.parquet")),
    ]


def test_read_pandas_csv():
    p = Path("dataframe.csv")
    with pytest.raises(OSError) as e:
        read_pandas(p)

    message = str(e.value)
    assert message.startswith("[Errno 2]")
    assert "No such file or directory" in message or "does not exist" in message


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
