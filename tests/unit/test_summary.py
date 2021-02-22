import numpy as np
import pandas as pd

from pandas_profiling.model.summary import get_table_stats


def test_get_table_stats_empty_df():
    s = pd.DataFrame({'A': []})
    table_stats = get_table_stats(s, {})
    assert table_stats["p_cells_missing"] == 0
    assert table_stats["n_duplicates"] == 0
    assert table_stats["p_duplicates"] == 0



