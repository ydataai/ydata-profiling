import numpy as np
import pandas as pd
import pytest

from pandas_profiling import ProfileReport


@pytest.fixture
def dataframe() -> pd.DataFrame:
    size = 1000
    time_steps = np.arange(size)

    return pd.DataFrame(
        {
            "ascending_sequence": time_steps,
            "descending_sequence": time_steps[::-1],
            "ascending_sequence_with_noise": [x + e for x, e in zip(time_steps, np.random.normal(10, 100, size))],
            "descending_sequence_with_noise": [x + e for x, e in zip(time_steps[::-1], np.random.normal(10, 100, size))],
            "ts_with_nan": [x if x % 4 != 0 else None for x in time_steps],
            "ts_negatives": -1 * time_steps,
            "constant": np.ones(size),
            "sin": map(lambda x: round(np.sin(x * np.pi / 180), 2), time_steps),
            "cos": map(lambda x: round(np.cos(x * np.pi / 180), 2), time_steps),
            "uniform": map(lambda x: round(x, 2), np.random.uniform(0, 10, size)),
            "gaussian": map(lambda x: round(x, 2), np.random.normal(0, 1, size)),
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
        html.count("role=tab data-toggle=tab>Autocorrelation<") == 8
    ), "TimeSeries incorrecly indentified"
