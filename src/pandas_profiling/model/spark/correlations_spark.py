"""Correlations between variables."""
from typing import Optional

import pandas as pd
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.stat import Correlation
from pyspark.sql import DataFrame

from pandas_profiling.config import Settings
from pandas_profiling.model.correlations import (
    Cramers,
    Kendall,
    Pearson,
    PhiK,
    Spearman,
)


@Spearman.compute.register(Settings, DataFrame, dict)
def spark_spearman_compute(
    config: Settings, df: DataFrame, summary: dict
) -> Optional[DataFrame]:
    variables = {column: description["type"] for column, description in summary.items()}
    interval_columns = [
        column for column, type_name in variables.items() if type_name == "Numeric"
    ]
    df = df.select(*interval_columns)

    # convert to vector column first
    vector_col = "corr_features"

    assembler = VectorAssembler(inputCols=df.columns, outputCol=vector_col, handleInvalid="skip")
    df_vector = assembler.transform(df).select(vector_col)

    # get correlation matrix
    matrix = (
        Correlation.corr(df_vector, vector_col, method="spearman").head()[0].toArray()
    )
    return pd.DataFrame(matrix, index=df.columns, columns=df.columns)


@Pearson.compute.register(Settings, DataFrame, dict)
def spark_pearson_compute(
    config: Settings, df: DataFrame, summary: dict
) -> Optional[DataFrame]:
    # convert to vector column first
    variables = {column: description["type"] for column, description in summary.items()}
    interval_columns = [
        column for column, type_name in variables.items() if type_name == "Numeric"
    ]
    df = df.select(*interval_columns)

    vector_col = "corr_features"
    assembler = VectorAssembler(inputCols=df.columns, outputCol=vector_col, handleInvalid="skip")
    df_vector = assembler.transform(df).select(vector_col)

    # get correlation matrix
    matrix = (
        Correlation.corr(df_vector, vector_col, method="pearson").head()[0].toArray()
    )
    return pd.DataFrame(matrix, index=df.columns, columns=df.columns)


@Kendall.compute.register(Settings, DataFrame, dict)
def spark_kendall_compute(
    config: Settings, df: DataFrame, summary: dict
) -> Optional[DataFrame]:
    raise NotImplementedError()


@Cramers.compute.register(Settings, DataFrame, dict)
def spark_cramers_compute(
    config: Settings, df: DataFrame, summary: dict
) -> Optional[DataFrame]:
    raise NotImplementedError()


@PhiK.compute.register(Settings, DataFrame, dict)
def spark_phi_k_compute(
    config: Settings, df: DataFrame, summary: dict
) -> Optional[DataFrame]:
    raise NotImplementedError()
