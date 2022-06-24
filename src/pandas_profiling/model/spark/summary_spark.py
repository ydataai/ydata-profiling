"""Compute statistical description of datasets."""
import multiprocessing
from typing import Tuple

import numpy as np
from pyspark.sql import DataFrame
from tqdm import tqdm
from visions import VisionsTypeset

from pandas_profiling.config import Settings
from pandas_profiling.model.summarizer import BaseSummarizer
from pandas_profiling.model.summary import describe_1d, get_series_descriptions
from pandas_profiling.utils.dataframe import sort_column_names


@describe_1d.register
def spark_describe_1d(
    config: Settings,
    series: DataFrame,
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

    # get `infer_dtypes` (bool) from config
    if config.infer_dtypes:
        # Infer variable types
        vtype = typeset.infer_type(series)
        series = typeset.cast_to_inferred(series)
    else:
        # Detect variable types from pandas dataframe (df.dtypes).
        # [new dtypes, changed using `astype` function are now considered]
        # vtype = typeset.detect_type(series)
        if str(series.schema[0].dataType).startswith("ArrayType"):
            dtype = "ArrayType"
        else:
            dtype = str(series.schema[0].dataType)
        vtype = {
            "IntegerType": "Numeric",
            "LongType": "Numeric",
            "ShortType": "Numeric",
            "ByteType": "Numeric",
            "DoubleType": "Numeric",
            "FloatType": "Numeric",
            "DecimalType": "Numeric",
            "StringType": "Categorical",
            "ArrayType": "Categorical",
            "BooleanType": "Boolean",
            "DateType": "DateTime",
            "TimestampType": "DateTime",
        }[dtype]

    return summarizer.summarize(config, series, dtype=vtype)


@get_series_descriptions.register
def spark_get_series_descriptions(
    config: Settings,
    df: DataFrame,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    pbar: tqdm,
) -> dict:
    series_description = {}

    def multiprocess_1d(args: tuple) -> Tuple[str, dict]:
        """Wrapper to process series in parallel.

        Args:
            column: The name of the column.
            series: The series values.

        Returns:
            A tuple with column and the series description.
        """
        column, df = args
        return column, describe_1d(config, df.select(column), summarizer, typeset)

    args = [(name, df) for name in df.columns]
    with multiprocessing.pool.ThreadPool(12) as executor:
        for i, (column, description) in enumerate(
            executor.imap_unordered(multiprocess_1d, args)
        ):
            pbar.set_postfix_str(f"Describe variable:{column}")
            series_description[column] = description
            pbar.update()
        series_description = {k: series_description[k] for k in df.columns}

    # Restore the original order
    # series_description = {k: series_description[k] for k in df.columns}
    # for col in df.columns:
    #     pbar.set_postfix_str(f"Describe variable:{col}")
    #     description = describe_1d(config, df.select(col), summarizer, typeset)
    #     series_description[col] = description
    #     pbar.update()

    # Mapping from column name to variable type
    series_description = sort_column_names(series_description, config.sort)
    return series_description
