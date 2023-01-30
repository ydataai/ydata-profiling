import pandas as pd

from ydata_profiling.model.table import get_table_stats


def test_get_table_stats_empty_df(config):
    df = pd.DataFrame({"A": [], "B": []})
    table_stats = get_table_stats(config, df, {})
    assert table_stats["n"] == 0
    assert table_stats["p_cells_missing"] == 0
