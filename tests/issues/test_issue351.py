import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.model.typeset import Unsupported


def test_issue351():
    data = pd.DataFrame(["Jan", 1]).set_index(0)

    profile = ProfileReport(data)
    assert (
        profile.get_description()["variables"]["0"]["type"]
        == Unsupported
    )
