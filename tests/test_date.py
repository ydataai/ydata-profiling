import pandas as pd
import pytest

import pandas_profiling


def check_date_type_warning():
    df = pd.DataFrame(["2018-01-01", "2017-02-01", "2018-04-07"], columns=["date"])

    with pytest.warns(
        UserWarning,
        match='Column "date" appears to be containing only date/datetime values',
    ):
        x = df.profile_report()

    assert "Categorical, Unique" in x.to_html()
