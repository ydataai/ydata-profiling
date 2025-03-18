"""Compute statistical description of datasets."""
from typing import Tuple

import numpy as np
from pyspark.sql import DataFrame
from tqdm import tqdm
from visions import VisionsTypeset

from ydata_profiling.config import Settings
from ydata_profiling.model.summarizer import BaseSummarizer
from ydata_profiling.utils.dataframe import sort_column_names


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

        if str(series.schema[0].dataType).startswith("ArrayType"):
            dtype = "ArrayType"
        else:
            dtype = series.schema[0].dataType.simpleString()

        vtype = {
            "float": "Numeric",
            "int": "Numeric",
            "bigint": "Numeric",
            "double": "Numeric",
            "string": "Categorical",
            "ArrayType": "Categorical",
            "boolean": "Boolean",
            "date": "DateTime",
            "timestamp": "DateTime",
        }[dtype]

    return summarizer.summarize(config, series, dtype=vtype)


def get_series_descriptions_spark(
    config: Settings,
    df: DataFrame,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    pbar: tqdm,
) -> dict:
    """
    Compute series descriptions/statistics for a Spark DataFrame.

    Returns: A dict with the series descriptions for each column of a Dataset
    """

    def describe_column(name: str) -> Tuple[str, dict]:
        """Process a single Spark column using Spark's execution model."""
        description = spark_describe_1d(config, df.select(name), summarizer, typeset)
        pbar.set_postfix_str(f"Describe variable: {name}")
        pbar.update()

        # Clean up Spark-specific metadata
        description.pop(
            "value_counts", None
        )  # Use `.pop()` with default to avoid KeyError
        return name, description

    series_description = {col: describe_column(col)[1] for col in df.columns}

    # Sort and return descriptions
    return sort_column_names(series_description, config.sort)
