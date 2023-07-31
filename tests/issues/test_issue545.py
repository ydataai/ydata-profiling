"""
Test for issue 545:
https://github.com/ydataai/ydata-profiling/issues/545
"""

from pathlib import Path

import pandas as pd
import pytest

from ydata_profiling import ProfileReport
from ydata_profiling.utils.compat import pandas_version_info


@pytest.mark.skipif(
    pandas_version_info() <= (1, 1, 0), reason="requires pandas 1.1.1 or higher"
)
def test_issue545():
    file_name = Path(__file__).parents[0] / "data/sample_eda_df.pkl"

    sample_eda_df = pd.read_pickle(str(file_name))
    sample_profile = ProfileReport(
        sample_eda_df,
        title="Sample Profiling Report",
        explorative=True,
        pool_size=1,
        progress_bar=False,
    )
    assert len(sample_profile.to_html()) > 0
