import pandas as pd
import pytest

from ydata_profiling import ProfileReport
from ydata_profiling.utils.compat import pandas_version_info


@pytest.fixture()
def df():
    df = pd.DataFrame(
        {
            "foo": [1, 2, 3],
            "bar": ["", "", ""],
        }
    )
    return df


@pytest.mark.skipif(
    pandas_version_info() < (2, 1, 0), reason="requires pandas 2.1 or higher"
)
def test_pd_future_infer_string(df: pd.DataFrame):
    with pd.option_context("future.infer_string", True):
        profile_report = ProfileReport(df, title="Test Report", progress_bar=False)
        assert len(profile_report.to_html()) > 0
