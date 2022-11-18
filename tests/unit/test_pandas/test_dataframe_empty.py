import pandas as pd
import pytest

from pandas_profiling import ProfileReport


@pytest.mark.parametrize(
    "test_data",
    [
        pd.DataFrame(),
        pd.DataFrame(["Jan", 1]).set_index(0),
        pd.DataFrame({"A": [], "B": []}),
    ],
)
def test_empty(test_data):
    profile = ProfileReport(test_data, progress_bar=False)
    description = profile.get_description()

    assert len(description["correlations"]) == 0
    assert len(description["missing"]) == 0

    html = profile.to_html()
    assert "Dataset is empty" in html
