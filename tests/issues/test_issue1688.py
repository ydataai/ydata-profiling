"""
Test for issue 1688.

https://github.com/ydataai/ydata-profiling/issues/1688

"""
import tempfile

import numpy as np
import pandas as pd
import pytest

from ydata_profiling import ProfileReport
from ydata_profiling.config import Settings
from ydata_profiling.utils.paths import get_config


@pytest.fixture
def data():
    """Creates a dataframe for the test."""
    data = [
        [1.0, 999, "", 10, None],
        [34.54, 3424, None, 4, 5],
        [9548.43, 1, "fdsfv", 54, 876],
        [32, 43.43, "dsfda", 43, 12],
        [1.0, 5454, "cxcc", 13, 43],
        [45.7, 43, "fsdfsfsfdsfsdf", 1, 54],
    ]

    df = pd.DataFrame(np.array(data), columns=["a", "b", "c", "d", "e"])

    return df


def test_empty_df(data):
    """Checking for an empty dataframe."""
    if not len(data):
        raise ValueError("Check the dataframe it is empty")


def test_issue1688(data):
    """
    Check: empty_df, report and html.

    Here, first the dataframe is checked to see if it is empty,
    then a report and temporary html are created,
    which is deleted after the block completes.
    """
    test_empty_df(data)

    conf = get_config("config_default.yaml")
    conf = Settings().from_file(conf)
    conf.plot.histogram.max_bins = 2
    conf.plot.histogram.bins = 0
    profile = ProfileReport(data, config=conf, title="Pandas Profiling Report")

    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        # Generate a temporary file and delete it
        # after the block is completed
        profile.to_file(temp_file.name)
