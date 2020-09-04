"""
Test for issue 537:
https://github.com/pandas-profiling/pandas-profiling/issues/537

ValueError: shape mismatch: value array of shape (136,) could not be broadcast to indexing result of shape (135,)

Problem :
ValueError is raised when running ProfileReport on large datasets and with multiprocessing on (pool_size >1).
This is likely due to the series.fillna(np.nan, inplace=True) in summary.py seems to be performing multiple in-place
mutations to the underlying DataFrame object through the passed series reference, resulting in some kind of race
condition where two of the processes try to write to the DataFrame at the same time and the ValueError then occurs.
 This is also why changing the pool_size to 1 fixes the issue, and why the error doesn't always occur -
 you probably need enough data and threads to hit the race condition.

Solution :
Replace series.fillna(np.nan, inplace=True) with series = series.fillna(np.nan) , negating any side effects from mutation.


"""

import multiprocessing
from functools import partial
from gzip import decompress
from typing import Tuple

import numpy as np
import pandas as pd
import requests

from pandas_profiling.model.summary import describe_1d


def mock_multiprocess_1d(args, summarizer, typeset) -> Tuple[str, dict]:
    """Wrapper to process series in parallel.
        copy of multiprocess_1d function in get_series_descriptions, summary.py

    Args:
        column: The name of the column.
        series: The series values.

    Returns:
        A tuple with column and the series description.
    """
    column, series = args
    return column, describe_1d(series, summarizer, typeset)


def test_multiprocessing_describe1d(summarizer, typeset):
    """
    this test serves to get a large dataset, and ensure that even across parallelised describe1d operations,
    there is no ValueError raised. Previously, series.fillna(np.nan,inplace=True) was used instead of
    series = series.fillna(np.nan) in model.summmary.describe1d, resulting in a race condition where the underlying
    df was being mutated by two threads at the same time creating a ValueError. This test checks that this does not
    occur again by running a parallelised describe1d and testing if a ValueError is raised.

    """

    def download_and_process_data():
        response = requests.get("https://ndownloader.figshare.com/files/5976042")
        assert response.status_code == 200
        file = decompress(response.content)
        text = file.decode()
        split_text = [i.split(",") for i in filter(lambda x: x, text.split("\n"))]
        dt = [
            ("duration", int),
            ("protocol_type", "S4"),
            ("service", "S11"),
            ("flag", "S6"),
            ("src_bytes", int),
            ("dst_bytes", int),
            ("land", int),
            ("wrong_fragment", int),
            ("urgent", int),
            ("hot", int),
            ("num_failed_logins", int),
            ("logged_in", int),
            ("num_compromised", int),
            ("root_shell", int),
            ("su_attempted", int),
            ("num_root", int),
            ("num_file_creations", int),
            ("num_shells", int),
            ("num_access_files", int),
            ("num_outbound_cmds", int),
            ("is_host_login", int),
            ("is_guest_login", int),
            ("count", int),
            ("srv_count", int),
            ("serror_rate", float),
            ("srv_serror_rate", float),
            ("rerror_rate", float),
            ("srv_rerror_rate", float),
            ("same_srv_rate", float),
            ("diff_srv_rate", float),
            ("srv_diff_host_rate", float),
            ("dst_host_count", int),
            ("dst_host_srv_count", int),
            ("dst_host_same_srv_rate", float),
            ("dst_host_diff_srv_rate", float),
            ("dst_host_same_src_port_rate", float),
            ("dst_host_srv_diff_host_rate", float),
            ("dst_host_serror_rate", float),
            ("dst_host_srv_serror_rate", float),
            ("dst_host_rerror_rate", float),
            ("dst_host_srv_rerror_rate", float),
            ("labels", "S16"),
        ]
        DT = np.dtype(dt)
        split_text = np.asarray(split_text, dtype=object)
        for j in range(42):
            split_text[:, j] = split_text[:, j].astype(DT[j])
        df = pd.DataFrame(split_text)
        return df

    def run_multiprocess(df):
        pool = multiprocessing.pool.ThreadPool(10)
        args = [(column, series) for column, series in df.iteritems()]
        results = pool.imap_unordered(
            partial(mock_multiprocess_1d, summarizer=summarizer, typeset=typeset), args
        )
        pool.close()
        pool.join()
        list(results)

    try:
        df = download_and_process_data()
        run_multiprocess(df)
    except ValueError:
        raise Exception("myFunc() raised ValueError unexpectedly!")
