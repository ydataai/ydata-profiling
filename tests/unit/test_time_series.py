import numpy as np
import pandas as pd
import pytest

from pandas_profiling import ProfileReport


@pytest.fixture
def html_profile() -> str:
    size = 1000
    time_steps = np.arange(size)

    df = pd.DataFrame(
        {
            "ascending_sequence": time_steps,
            "descending_sequence": time_steps[::-1],
            "ascending_sequence_with_noise": [
                x + e for x, e in zip(time_steps, np.random.normal(5, 30, size))
            ],
            "descending_sequence_with_noise": [
                x + e for x, e in zip(time_steps[::-1], np.random.normal(5, 30, size))
            ],
            "ts_with_nan": [x if x % 4 != 0 else None for x in time_steps],
            "ts_negatives": -1 * time_steps,
            "constant": np.ones(size),
            "sin": [round(np.sin(x * np.pi / 180), 2) for x in time_steps],
            "cos": [round(np.cos(x * np.pi / 180), 2) for x in time_steps],
            "uniform": [round(x, 2) for x in np.random.uniform(0, 10, size)],
            "gaussian": [round(x, 2) for x in np.random.normal(0, 1, size)],
        }
    )

    profile = ProfileReport(df, tsmode=True)
    return profile.to_html()


def test_timeseries_identification(html_profile: str):
    assert "<th>TimeSeries</th>" in html_profile, "TimeSeries not detected"
    assert (
        "<tr><th>TimeSeries</th><td>8</td></tr>" in html_profile
    ), "TimeSeries incorrectly identified"


def test_timeseries_autocorrelation_tab(html_profile: str):
    assert (
        "role=tab data-toggle=tab>Autocorrelation<" in html_profile
    ), "TimeSeries not detected"
    assert (
        html_profile.count("role=tab data-toggle=tab>Autocorrelation<") == 8
    ), "TimeSeries autocorrelation tabs incorrectly generated"


def test_timeseries_seasonality(html_profile: str):
    assert (
        html_profile.count("<code>SEASONAL</code>") == 2
    ), "Seasonality incorrectly identified"
    assert (
        html_profile.count(">Seasonal</span>") == 2
    ), "Seasonality warning incorrectly identified"
