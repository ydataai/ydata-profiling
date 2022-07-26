import numpy as np
import pandas as pd
import pytest

from pandas_profiling import ProfileReport


@pytest.fixture
def dataframe() -> pd.DataFrame:
    size = 20
    return pd.DataFrame(
        {
            "ts": np.arange(size),
            "reverse": reversed(np.arange(size)),
            "ts_with_nan": [x if x % 4 != 0 else None for x in np.arange(size)],
            "ts_negatives": -1 * np.arange(size),
            "non_ts": np.ones(20),
        }
    )


def test_timeseries(dataframe):
    profile = ProfileReport(dataframe, tsmode=True)
    html = profile.to_html()
    assert "<th>TimeSeries</th>" in html, "TimeSeries not detected"
    assert (
        "role=tab data-toggle=tab>Autocorrelation<" in html
    ), "TimeSeries not detected"
    assert (
        html.count("role=tab data-toggle=tab>Autocorrelation<") == 4
    ), "TimeSeries incorrecly indentified"
