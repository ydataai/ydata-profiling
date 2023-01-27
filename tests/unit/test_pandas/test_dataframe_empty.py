import pandas as pd
import pytest

from ydata_profiling import ProfileReport


@pytest.mark.parametrize(
    "test_data",
    [
        pd.DataFrame(),
        pd.DataFrame(["Jan", 1]).set_index(0),
        pd.DataFrame({"A": [], "B": []}),
    ],
)
def test_empty(test_data):
    with pytest.raises(ValueError):
        ProfileReport(test_data, progress_bar=False)
