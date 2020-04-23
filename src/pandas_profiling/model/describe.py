import warnings

import pandas as pd
from tqdm.auto import tqdm

from pandas_profiling.config import config as config
from pandas_profiling.model.summary import (
    get_series_descriptions,
    get_scatter_matrix,
    get_table_stats,
    get_missing_diagrams,
    get_messages,
    sort_column_names,
    get_series_description,
)
from pandas_profiling.model.correlations import calculate_correlation
from pandas_profiling.version import __version__


def describe(df: pd.DataFrame) -> dict:
    """Calculate the statistics for each series in this DataFrame.

    Args:
        df: DataFrame.

    Returns:
        This function returns a dictionary containing:
            - table: overall statistics.
            - variables: descriptions per series.
            - correlations: correlation matrices.
            - missing: missing value diagrams.
            - messages: direct special attention to these patterns in your data.
    """

    """ Those items with * make up description_set
    +-------------------------------------------------------------+         +-------------+
    |                       DataFrame                             |         |  Package*   |
    +--+--------------+----------------+--------------+--------+--+         +-------------+
       |              v                |              |        |
       |     +--------+-------------+  |              |        |
       |     |  series_description* |  |              |        |
       |     +-----+--------------+-+  |              |        |
       |           v              v    |              |        |
       |     +-----+-----+    +---+------------+      |        |
       |     | variables |    | variable_stats |      |        |
       |     +-+----+----+    +-------------+--+      |        |
       |       |    |                  |    |         |        |
       v       v    +---------v   v----+    +------v  v        |
      ++-------+-----+   +----+---+------+    +----+--+-----+  |
      |correlations* |   |scatter_matrix*|    |table_stats* |  |
      +---+----------+   +------+--------+    +--+--------+-+  |
          v                     v                v        v    v
      +---+---------------------+----------------+--+ +---+----+--+
      |               messages*                     | |  missing* |
      +---------------------------------------------+ +-----------+
    """

    if not isinstance(df, pd.DataFrame):
        warnings.warn("df is not of type pandas.DataFrame")

    if df.empty:
        raise ValueError("df can not be empty")

    disable_progress_bar = not config["progress_bar"].get(bool)

    correlation_names = [
        correlation_name
        for correlation_name in [
            "pearson",
            "spearman",
            "kendall",
            "phi_k",
            "cramers",
            "recoded",
        ]
        if config["correlations"][correlation_name]["calculate"].get(bool)
    ]

    number_of_task = 7 + len(df.columns) + len(correlation_names)

    with tqdm(
        total=number_of_task, desc="Describe", disable=disable_progress_bar
    ) as pbar:
        series_description = get_series_descriptions(df, pbar)
        # Mapping from column name to variable type
        sort = config["sort"].get(str)
        series_description = sort_column_names(series_description, sort)

        pbar.set_postfix_str("Get variable types")
        variables = {
            column: description["type"]
            for column, description in series_description.items()
        }
        pbar.update()

        # Transform the series_description in a DataFrame
        pbar.set_postfix_str("Get variable statistics")
        variable_stats = pd.DataFrame(series_description)
        pbar.update()

        # Get correlations
        correlations = {}
        for correlation_name in correlation_names:
            pbar.set_postfix_str(f"Calculate {correlation_name} correlation")
            correlations[correlation_name] = calculate_correlation(
                df, variables, correlation_name
            )
            pbar.update()
        correlations = {
            key: value for key, value in correlations.items() if value is not None
        }

        # Scatter matrix
        pbar.set_postfix_str("Get scatter matrix")
        scatter_matrix = get_scatter_matrix(df, variables)
        pbar.update()

        # Table statistics
        pbar.set_postfix_str("Get table statistics")
        table_stats = get_table_stats(df, variable_stats)
        pbar.update()

        # missing diagrams
        pbar.set_postfix_str("Get missing diagrams")
        missing = get_missing_diagrams(df, table_stats)
        pbar.update()

        # Messages
        pbar.set_postfix_str("Get messages")
        messages = get_messages(table_stats, series_description, correlations)
        pbar.update()

        pbar.set_postfix_str("Get package info")
        package = {
            "pandas_profiling_version": __version__,
            "pandas_profiling_config": config.dump(),
        }
        pbar.update()
        pbar.set_postfix_str("Finished")

    return {
        # Overall description
        "table": table_stats,
        # Per variable descriptions
        "variables": series_description,
        # Bivariate relations
        "scatter": scatter_matrix,
        # Correlation matrices
        "correlations": correlations,
        # Missing values
        "missing": missing,
        # Warnings
        "messages": messages,
        # Package
        "package": package,
    }
