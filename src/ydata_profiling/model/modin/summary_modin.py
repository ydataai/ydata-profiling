"""Compute statistical description of datasets."""

from typing import Tuple

import numpy as np
from tqdm import tqdm
from visions import VisionsTypeset

from ydata_profiling.config import Settings
from ydata_profiling.model.summarizer import BaseSummarizer
from ydata_profiling.model.summary import describe_1d, get_series_descriptions
from ydata_profiling.model.typeset import ProfilingTypeSet
from ydata_profiling.utils import modin
from ydata_profiling.utils.dataframe import sort_column_names


@describe_1d.register
def modin_describe_1d(
    config: Settings,
    series: modin.Series,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
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

    if (
        isinstance(typeset, ProfilingTypeSet)
        and typeset.type_schema
        and series.name in typeset.type_schema
    ):
        vtype = typeset.type_schema[series.name]
    elif config.infer_dtypes:
        # Infer variable types
        series = series._to_pandas()
        vtype = typeset.infer_type(series)
        series = typeset.cast_to_inferred(series)
        series = modin.Series(series)
    else:
        # Detect variable types from pandas dataframe (df.dtypes).
        # [new dtypes, changed using `astype` function are now considered]
        vtype = typeset.detect_type(series)

    typeset.type_schema[series.name] = vtype
    return summarizer.summarize(config, series, dtype=vtype)


@get_series_descriptions.register
def modin_get_series_descriptions(
    config: Settings,
    df: modin.DataFrame,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    pbar: tqdm,
) -> dict:
    def multiprocess_1d(args: tuple) -> Tuple[str, dict]:
        """Wrapper to process series in parallel.

        Args:
            column: The name of the column.
            series: The series values.

        Returns:
            A tuple with column and the series description.
        """
        column, series = args
        return column, describe_1d(config, series, summarizer, typeset)

    args = [(name, series) for name, series in df.items()]
    series_description = {}

    for arg in args:
        pbar.set_postfix_str(f"Describe variable:{arg[0]}")
        column, description = multiprocess_1d(arg)
        series_description[column] = description
        pbar.update()

    # Mapping from column name to variable type
    series_description = sort_column_names(series_description, config.sort)
    return series_description
