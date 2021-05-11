"""
Test for issue 416:
https://github.com/pandas-profiling/pandas-profiling/issues/416
"""
import pandas as pd

import pandas_profiling
from pandas_profiling.utils.cache import cache_file


def test_issue416():
    file_name = cache_file(
        "products.tsv",
        "https://raw.githubusercontent.com/mrichman/clickstream-pandas/master/products.tsv",
    )

    df = pd.read_csv(file_name, sep="\t")
    df["path"] = df["url"].str.replace("http://www.acme.com", "", regex=False)

    profile = pandas_profiling.ProfileReport(
        df,
        title="Pandas Profiling Report",
        html={"style": {"full_width": True}},
        explorative=True,
    )
    data = profile.get_description()

    assert data["table"]["types"]["Categorical"] == 1
    assert data["table"]["types"]["Path"] == 1
    assert data["table"]["types"]["URL"] == 1
    assert data["variables"]["path"]["common_prefix"] == "/"
