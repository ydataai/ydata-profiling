"""Compute statistical description of datasets."""

import multiprocessing
import multiprocessing.pool
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
from pandas_profiling.config import Settings
from pandas_profiling.model.summarizer import BaseSummarizer
from pandas_profiling.model.summary import describe_1d, get_series_descriptions
from pandas_profiling.utils.dataframe import sort_column_names
from tqdm import tqdm
from visions import VisionsTypeset


@describe_1d.register
def pandas_describe_1d(
    config: Settings,
    series: pd.Series,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    target_col: Optional[pd.Series] = None,
) -> dict:
    """Describe a series (infer the variable type, then calculate type-specific values).

    Args:
        config: report Settings object
        series: The Series to describe.
        summarizer: Summarizer object
        typeset: Typeset

    Returns:
        A Series containing calculated series description values.
    """

    # Make sure pd.NA is not in the series
    series = series.fillna(np.nan)

    # get `infer_dtypes` (bool) from config
    if config.infer_dtypes:
        # Infer variable types
        vtype = typeset.infer_type(series)
        series = typeset.cast_to_inferred(series)
    else:
        # Detect variable types from pandas dataframe (df.dtypes).
        # [new dtypes, changed using `astype` function are now considered]
        vtype = typeset.detect_type(series)

    return summarizer.summarize(config, series, dtype=vtype, target_col=target_col)


@get_series_descriptions.register
def pandas_get_series_descriptions(
    config: Settings,
    df: pd.DataFrame,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    pbar: tqdm,
) -> Dict[str, Any]:
    def multiprocess_1d(args: Tuple[str, pd.Series]) -> Tuple[str, dict]:
        """Wrapper to process series in parallel.

        Args:
            column: The name of the column.
            series: The series values.

        Returns:
            A tuple with column and the series description.
        """
        column, series = args
        return column, describe_1d(config, series, summarizer, typeset, target_col)

    pool_size = config.pool_size

    if config.target_col is not None:
        target_col = df[config.target_col].astype(str)
    else:
        target_col = None

    # Multiprocessing of Describe 1D for each column
    if pool_size <= 0:
        pool_size = multiprocessing.cpu_count()

    args = [(name, series) for name, series in df.items()]
    series_description = {}

    if pool_size == 1:
        for arg in args:
            pbar.set_postfix_str(f"Describe variable:{arg[0]}")
            column, description = multiprocess_1d(arg)
            series_description[column] = description
            pbar.update()
    else:
        # TODO: use `Pool` for Linux-based systems
        with multiprocessing.pool.ThreadPool(pool_size) as executor:
            for i, (column, description) in enumerate(
                executor.imap_unordered(multiprocess_1d, args)
            ):
                pbar.set_postfix_str(f"Describe variable:{column}")
                series_description[column] = description
                pbar.update()

        # Restore the original order
        series_description = {k: series_description[k] for k in df.columns}

    # Mapping from column name to variable type
    series_description = sort_column_names(series_description, config.sort)
    return series_description
