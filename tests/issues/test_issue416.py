"""
Test for issue 416:
https://github.com/pandas-profiling/pandas-profiling/issues/416
"""
import pandas as pd
import pytest

import pandas_profiling
from pandas_profiling.utils.cache import cache_file


@pytest.mark.linux
def test_issue416():
    file_name = cache_file(
        "products.tsv",
        "https://raw.githubusercontent.com/mrichman/clickstream-pandas/master/products.tsv",
    )

    df = pd.read_csv(file_name, sep="\t")
    df["path"] = df["url"].str.replace("http://www.acme.com", "")

    profile = pandas_profiling.ProfileReport(
        df, title="Pandas Profiling Report", html={"style": {"full_width": True}}
    )
    data = profile.to_json()
    assert '"Path": 1' in data
    assert '"common_prefix": "/",' in data
