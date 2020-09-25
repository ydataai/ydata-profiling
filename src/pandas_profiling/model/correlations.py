"""Correlations between variables."""
import itertools
import warnings
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import phik
from pandas.core.base import DataError
from scipy import stats
from singledispatchmethod import singledispatchmethod

from pandas_profiling.config import config
from pandas_profiling.model.dataframe_wrappers import (
    GenericDataFrame,
    PandasDataFrame,
    SparkDataFrame,
)
from pandas_profiling.model.typeset import Boolean, Categorical, Numeric, Unsupported


class Correlation:
    @singledispatchmethod
    @staticmethod
    def compute(df, summary):
        df_type = type(df)
        raise NotImplementedError(f"Not Implementated for dataframe_type {df_type}")

    @compute.register(PandasDataFrame)
    @staticmethod
    def _(df: PandasDataFrame, summary) -> Optional[pd.DataFrame]:
        return NotImplemented


class Spearman(Correlation):
    @singledispatchmethod
    @staticmethod
    def compute(df, summary):
        df_type = type(df)
        raise NotImplementedError(f"Not Implementated for dataframe_type {df_type}")

    @compute.register(PandasDataFrame)
    @staticmethod
    def _(df: PandasDataFrame, summary) -> Optional[pd.DataFrame]:
        return df.get_pandas_df().corr(method="spearman")

    @compute.register(SparkDataFrame)
    @staticmethod
    def _(df: SparkDataFrame, summary) -> Optional[pd.DataFrame]:
        """
        TODO - Optimise this in Spark, cheating for now

        Args:
            df:
            summary:

        Returns:

        """
        from pyspark.ml.feature import VectorAssembler
        from pyspark.ml.stat import Correlation

        # get all columns in df that are numeric as spearman works only on numeric columns
        numeric_columns = df.get_numeric_columns()

        # assemble all numeric columns into a vector
        assembler = VectorAssembler(inputCols=numeric_columns, outputCol="features")
        output_df = assembler.transform(df.get_spark_df())

        # perform correlation in spark, and get the results back in pandas
        df = pd.DataFrame(
            Correlation.corr(output_df, "features", "spearman").head()[0].toArray(),
            columns=numeric_columns,
            index=numeric_columns,
        )

        return df


class Pearson(Correlation):
    @singledispatchmethod
    @staticmethod
    def compute(df, summary):
        df_type = type(df)
        raise NotImplementedError(f"Not Implemented for dataframe_type {df_type}")

    @compute.register(PandasDataFrame)
    @staticmethod
    def _(df: PandasDataFrame, summary) -> Optional[pd.DataFrame]:
        return df.get_pandas_df().corr(method="pearson")

    @compute.register(SparkDataFrame)
    @staticmethod
    def _(df: SparkDataFrame, summary) -> Optional[pd.DataFrame]:
        """
        TODO - Optimise this in Spark, cheating for now

        Args:
            df:
            summary:

        Returns:

        """
        from pyspark.ml.feature import VectorAssembler
        from pyspark.ml.stat import Correlation

        # get all columns in df that are numeric as pearson works only on numeric columns
        numeric_columns = df.get_numeric_columns()

        # assemble all numeric columns into a vector
        assembler = VectorAssembler(inputCols=numeric_columns, outputCol="features")
        output_df = assembler.transform(df.get_spark_df())

        # perform correlation in spark, and get the results back in pandas
        df = pd.DataFrame(
            Correlation.corr(output_df, "features", "pearson").head()[0].toArray(),
            columns=numeric_columns,
            index=numeric_columns,
        )
        return df


class Kendall(Correlation):
    @singledispatchmethod
    @staticmethod
    def compute(df, summary):
        df_type = type(df)
        raise NotImplementedError(f"Not Implemented for dataframe_type {df_type}")

    @compute.register(PandasDataFrame)
    @staticmethod
    def _(df: PandasDataFrame, summary) -> Optional[pd.DataFrame]:
        return df.get_pandas_df().corr(method="kendall")

    @compute.register(SparkDataFrame)
    @staticmethod
    def _(df: SparkDataFrame, summary) -> Optional[pd.DataFrame]:
        """
        this can probably be improved more, primarily because we need to shuffle all numeric columns to
        a single node now. We need an algorithm to do distributed kendalls at each node (some form of vectorized sort
        bin function, and then aggregate the results afterwards? It looks like some algos are out there,
        but stretch goal for now I suppose.
        See https://arxiv.org/abs/1704.03767

        Args:
            df:
            summary:

        Returns:

        """

        from pyspark.sql.functions import PandasUDFType, col, lit, pandas_udf
        from pyspark.sql.types import (
            DoubleType,
            FloatType,
            IntegerType,
            LongType,
            StringType,
            StructField,
            StructType,
        )

        # get all columns in df that are numeric as kendall works only on numeric columns
        numeric_columns = df.get_numeric_columns()

        # generate output schema for pandas_udf
        output_schema_components = []
        for column in numeric_columns:
            output_schema_components.append(StructField(column, DoubleType(), True))
        output_schema = StructType(output_schema_components)

        # pandas mapped udf works only with a groupby, we force the groupby to operate on all columns at once
        # by giving one value to all columns
        groupby_df = (
            df.get_spark_df().select(numeric_columns).withColumn("groupby", lit(1))
        )

        # create the pandas grouped map function to do vectorized kendall within spark itself
        @pandas_udf(output_schema, PandasUDFType.GROUPED_MAP)
        def spark_kendall(pdf):
            # groupby enters the UDF, so we need to drop it then do the correlation
            results_df = (
                pdf.drop(columns=["groupby"])
                .corr(method="kendall", min_periods=1)
                .reset_index(drop=True)
            )
            return results_df

        # return the appropriate dataframe (similar to pandas_df.corr results)
        df = pd.DataFrame(
            groupby_df.groupby("groupby").apply(spark_kendall).toPandas().values,
            columns=numeric_columns,
            index=numeric_columns,
        )

        return df


class Cramers(Correlation):
    @staticmethod
    def _cramers_corrected_stat(confusion_matrix, correction: bool) -> float:
        """Calculate the Cramer's V corrected stat for two variables.

        Args:
            confusion_matrix: Crosstab between two variables.
            correction: Should the correction be applied?

        Returns:
            The Cramer's V corrected stat for the two variables.
        """
        chi2 = stats.chi2_contingency(confusion_matrix, correction=correction)[0]
        n = confusion_matrix.sum().sum()
        phi2 = chi2 / n
        r, k = confusion_matrix.shape

        # Deal with NaNs later on
        with np.errstate(divide="ignore", invalid="ignore"):
            phi2corr = max(0.0, phi2 - ((k - 1.0) * (r - 1.0)) / (n - 1.0))
            rcorr = r - ((r - 1.0) ** 2.0) / (n - 1.0)
            kcorr = k - ((k - 1.0) ** 2.0) / (n - 1.0)
            corr = np.sqrt(phi2corr / min((kcorr - 1.0), (rcorr - 1.0)))
        return corr

    @singledispatchmethod
    @staticmethod
    def compute(df, summary):
        df_type = type(df)
        raise NotImplementedError(f"Not Implementated for dataframe_type {df_type}")

    @compute.register(PandasDataFrame)
    @staticmethod
    def _(df: PandasDataFrame, summary) -> Optional[pd.DataFrame]:
        threshold = config["categorical_maximum_correlation_distinct"].get(int)

        categoricals = {
            key
            for key, value in summary.items()
            if value["type"] in {Categorical, Boolean}
            and value["n_distinct"] <= threshold
        }

        if len(categoricals) <= 1:
            return None

        matrix = np.zeros((len(categoricals), len(categoricals)))
        np.fill_diagonal(matrix, 1.0)
        correlation_matrix = pd.DataFrame(
            matrix,
            index=categoricals,
            columns=categoricals,
        )

        for name1, name2 in itertools.combinations(categoricals, 2):
            confusion_matrix = pd.crosstab(
                df.get_pandas_df()[name1], df.get_pandas_df()[name2]
            )
            correlation_matrix.loc[name2, name1] = Cramers._cramers_corrected_stat(
                confusion_matrix, correction=True
            )
            correlation_matrix.loc[name1, name2] = correlation_matrix.loc[name2, name1]
        return correlation_matrix

    @compute.register(SparkDataFrame)
    @staticmethod
    def _(df: SparkDataFrame, summary) -> Optional[pd.DataFrame]:
        """
        TODO - Optimise this in Spark, cheating for now

        Args:
            df:
            summary:

        Returns:

        """
        return Cramers.compute(PandasDataFrame(df.get_spark_df().toPandas()), summary)


class PhiK(Correlation):
    @singledispatchmethod
    @staticmethod
    def compute(df, summary):
        df_type = type(df)
        raise NotImplementedError(f"Not Implementated for dataframe_type {df_type}")

    @compute.register(PandasDataFrame)
    @staticmethod
    def _(df: PandasDataFrame, summary) -> Optional[pd.DataFrame]:
        threshold = config["categorical_maximum_correlation_distinct"].get(int)
        intcols = {
            key
            for key, value in summary.items()
            # DateTime currently excluded
            # In some use cases, it makes sense to convert it to interval
            # See https://github.com/KaveIO/PhiK/issues/7
            if value["type"] == Numeric and 1 < value["n_distinct"]
        }

        selcols = {
            key
            for key, value in summary.items()
            if value["type"] != Unsupported and 1 < value["n_distinct"] <= threshold
        }
        selcols = selcols.union(intcols)

        if len(selcols) <= 1:
            return None

        pandas_df = df.get_pandas_df()
        correlation = pandas_df[selcols].phik_matrix(interval_cols=intcols)

        return correlation

    @compute.register(SparkDataFrame)
    @staticmethod
    def _(df: SparkDataFrame, summary) -> Optional[pd.DataFrame]:
        """
        TODO - Optimise this in Spark, cheating for now
        Args:
            df:
            summary:

        Returns:

        """
        return PhiK.compute(PandasDataFrame(df.get_spark_df().toPandas()), summary)


def warn_correlation(correlation_name: str, error):
    warnings.warn(
        f"""There was an attempt to calculate the {correlation_name} correlation, but this failed.
To hide this warning, disable the calculation
(using `df.profile_report(correlations={{\"{correlation_name}\": {{\"calculate\": False}}}})`
If this is problematic for your use case, please report this as an issue:
https://github.com/pandas-profiling/pandas-profiling/issues
(include the error message: '{error}')"""
    )


def calculate_correlation(
    df: GenericDataFrame, correlation_name: str, summary
) -> Optional[pd.DataFrame]:
    """Calculate the correlation coefficients between variables for the correlation types selected in the config
    (pearson, spearman, kendall, phi_k, cramers).

    Args:
        variables: A dict with column names and variable types.
        df: The DataFrame with variables.
        correlation_name:

    Returns:
        The correlation matrices for the given correlation measures. Return None if correlation is empty.
    """

    correlation_measures = {
        "pearson": Pearson,
        "spearman": Spearman,
        "kendall": Kendall,
        "cramers": Cramers,
        "phi_k": PhiK,
    }

    correlation = None
    try:
        correlation = correlation_measures[correlation_name].compute(df, summary)
    except (ValueError, AssertionError, TypeError, DataError, IndexError) as e:
        warn_correlation(correlation_name, e)

    if correlation is not None and len(correlation) <= 0:
        correlation = None

    return correlation


def perform_check_correlation(
    correlation_matrix: pd.DataFrame, threshold: float
) -> Dict[str, List[str]]:
    """Check whether selected variables are highly correlated values in the correlation matrix.

    Args:
        correlation_matrix: The correlation matrix for the DataFrame.
        threshold:.

    Returns:
        The variables that are highly correlated.
    """

    cols = correlation_matrix.columns
    bool_index = abs(correlation_matrix.values) >= threshold
    np.fill_diagonal(bool_index, False)
    return {
        col: cols[bool_index[i]].values.tolist()
        for i, col in enumerate(cols)
        if any(bool_index[i])
    }
