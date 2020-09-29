"""Correlations between variables."""
import itertools
import warnings
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from pandas.core.base import DataError
from scipy import stats
from singledispatchmethod import singledispatchmethod

from pandas_profiling.config import config
from pandas_profiling.model.dataframe_wrappers import (
    GenericDataFrame,
    PandasDataFrame,
    SparkDataFrame,
)
from pandas_profiling.model.typeset import (
    Boolean,
    Categorical,
    Numeric,
    SparkCategorical,
    SparkNumeric,
    Unsupported,
)


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

        if len(numeric_columns) <= 1:
            # Can't compute correlations with 1 or less columns
            return None

        # assemble all numeric columns into a vector
        assembler = VectorAssembler(inputCols=numeric_columns, outputCol="features")
        output_df = assembler.transform(df.get_spark_df().na.drop())

        if len(output_df.head(1)) > 0:
            # perform correlation in spark, and get the results back in pandas
            return pd.DataFrame(
                Correlation.corr(output_df, "features", "spearman").head()[0].toArray(),
                columns=numeric_columns,
                index=numeric_columns,
            )
        else:
            return None


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

        if len(numeric_columns) <= 1:
            # Can't compute correlations with 1 or less columns
            return None

        # assemble all numeric columns into a vector
        assembler = VectorAssembler(inputCols=numeric_columns, outputCol="features")
        output_df = assembler.transform(df.get_spark_df().na.drop())

        # perform correlation in spark, and get the results back in pandas
        if len(output_df.head(1)) > 0:
            # perform correlation in spark, and get the results back in pandas
            return pd.DataFrame(
                Correlation.corr(output_df, "features", "pearson").head()[0].toArray(),
                columns=numeric_columns,
                index=numeric_columns,
            )
        else:
            return None


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
        Use pandasUDF to compute this first, but probably can be optimised further

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

        from pyspark.sql.functions import PandasUDFType, lit, pandas_udf
        from pyspark.sql.types import DoubleType, StructField, StructType

        # get all columns in df that are numeric as kendall works only on numeric columns
        numeric_columns = df.get_numeric_columns()

        if len(numeric_columns) <= 1:
            # Can't compute correlations with 1 or less columns
            return pd.DataFrame()

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
        if len(groupby_df.head(1)) > 0:
            # perform correlation in spark, and get the results back in pandas
            df = pd.DataFrame(
                groupby_df.groupby("groupby").apply(spark_kendall).toPandas().values,
                columns=numeric_columns,
                index=numeric_columns,
            )
        else:
            df = pd.DataFrame()

        return df


class Cramers(Correlation):
    @staticmethod
    def _cramers_corrected_stat(
        confusion_matrix=None, correction: bool = True, precomputed={}
    ) -> float:
        """Calculate the Cramer's V corrected stat for two variables.

        Args:
            confusion_matrix: Crosstab between two variables.
            correction: Should the correction be applied?
            precomputed: if chi2, n, r and k have been precomputed, just use those values, if not compute using
                        confusion matrix

        Returns:
            The Cramer's V corrected stat for the two variables.
        """
        if precomputed:
            try:
                chi2 = precomputed["chi2"]
                n = precomputed["n"]
                phi2 = chi2 / n
                r, k = precomputed["r"], precomputed["k"]
            except KeyError as e:
                raise KeyError(
                    f""" attempted to provide precomputed chi2, n, r and k values,
                                to _cramers_corrected_stat, but at least one value
                                was not provided. Original Error : {e}"""
                )
        else:
            if not confusion_matrix:
                raise ValueError(
                    "confusion matrix must be specificed if precomputed matrix not provided"
                )
            chi2 = stats.chi2_contingency(confusion_matrix, correction=correction)[0]
            n = confusion_matrix.sum().sum()
            phi2 = chi2 / n
            r, k = confusion_matrix.shape

        # compute correlation statistic
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

        Args:
            df:
            summary:

        Returns:

        """
        from pyspark.ml.feature import StringIndexer, VectorAssembler
        from pyspark.ml.stat import ChiSquareTest

        threshold = config["categorical_maximum_correlation_distinct"].get(int)

        categoricals = [
            key
            for key, value in summary.items()
            if value["type"] == SparkCategorical and value["n_distinct"] <= threshold
        ]

        if len(categoricals) <= 1:
            return None

        # prepare output matrix (same as in pandas)
        matrix = np.zeros((len(categoricals), len(categoricals)))
        np.fill_diagonal(matrix, 1.0)
        correlation_matrix = pd.DataFrame(
            matrix,
            index=categoricals,
            columns=categoricals,
        )

        # get categorical dataframe from spark
        categorical_df = df.get_spark_df().select(categoricals)

        # convert all categorical columns to string indexes, overriding categorical_df
        index_store = []
        for categorical_col in categoricals:
            # generate dictionary of index names
            index_col = categorical_col + "_cat"
            index_store.append({"original": categorical_col, "indexed": index_col})

            # create column of encoded strings for categorical column
            assembler = StringIndexer(inputCol=categorical_col, outputCol=index_col)
            categorical_df = assembler.fit(categorical_df).transform(categorical_df)

        # using persist on transformed columns of categorical_df here because we call on it multiple times below
        # persisting only the numerical columns saves us a lot of memory
        categorical_df = categorical_df.select([i["indexed"] for i in index_store])
        categorical_df.persist()

        # compute n for cramers once
        n_rows = categorical_df.count()

        # compute distinct counts once and reuse results later
        distinct_counts = {}
        for col in index_store:
            distinct_counts[col["indexed"]] = (
                categorical_df.select(col["indexed"]).distinct().count()
            )

        # for each categorical column
        for col in index_store:
            # get the other categorical columns to compare with
            input_cols = [i for i in index_store]
            input_cols.remove(col)
            index_input_cols_with_col_removed = [i["indexed"] for i in input_cols]

            # assemble all other vectors at once to do comparison
            assembler = VectorAssembler(
                inputCols=index_input_cols_with_col_removed, outputCol="feature"
            )
            temp_df = assembler.transform(categorical_df)

            # compute chisquare for between original categorical and all other columns
            chi_sq_result = ChiSquareTest.test(temp_df, "feature", col["indexed"])

            # zip results with relevant columns
            chi_squares = zip(
                input_cols, [i for i in chi_sq_result.collect()[0]["statistics"]]
            )

            # use computed chi_square values to compute cramers statistic
            for other_col, chisq in chi_squares:
                precomputed = {}
                precomputed["chi2"] = chisq
                precomputed["n"] = n_rows
                precomputed["r"] = distinct_counts[col["indexed"]]
                precomputed["k"] = distinct_counts[other_col["indexed"]]

                # when saving results, use back original col names
                correlation_matrix.loc[
                    other_col["original"], col["original"]
                ] = Cramers._cramers_corrected_stat(
                    confusion_matrix=None, correction=True, precomputed=precomputed
                )
                correlation_matrix.loc[
                    col["original"], other_col["original"]
                ] = correlation_matrix.loc[other_col["original"], col["original"]]

        # unpersisting to free memory
        categorical_df.unpersist()

        return correlation_matrix


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

        import phik

        correlation = phik.phik_matrix(
            df=pandas_df[selcols], interval_cols=list(intcols)
        )

        return correlation

    @compute.register(SparkDataFrame)
    @staticmethod
    def _(df: SparkDataFrame, summary) -> Optional[pd.DataFrame]:
        """
        Use pandasUDF to compute this first, but probably can be optimised further

        Args:
            df:
            summary:

        Returns:

        """
        from pyspark.sql.functions import PandasUDFType, lit, pandas_udf
        from pyspark.sql.types import DoubleType, StructField, StructType

        threshold = config["categorical_maximum_correlation_distinct"].get(int)
        intcols = {
            key
            for key, value in summary.items()
            # DateTime currently excluded
            # In some use cases, it makes sense to convert it to interval
            # See https://github.com/KaveIO/PhiK/issues/7
            if value["type"] == SparkNumeric and 1 < value["n_distinct"]
        }

        selcols = {
            key
            for key, value in summary.items()
            if value["type"] != Unsupported and 1 < value["n_distinct"] <= threshold
        }
        selcols = list(selcols.union(intcols))

        if len(selcols) <= 1:
            return None

        # pandas mapped udf works only with a groupby, we force the groupby to operate on all columns at once
        # by giving one value to all columns
        groupby_df = df.get_spark_df().select(selcols).withColumn("groupby", lit(1))

        # generate output schema for pandas_udf
        output_schema_components = []
        for column in selcols:
            output_schema_components.append(StructField(column, DoubleType(), True))
        output_schema = StructType(output_schema_components)

        # create the pandas grouped map function to do vectorized kendall within spark itself
        @pandas_udf(output_schema, PandasUDFType.GROUPED_MAP)
        def spark_phik(pdf):
            import phik

            correlation = phik.phik_matrix(df=pdf, interval_cols=list(intcols))
            return correlation

        # return the appropriate dataframe (similar to pandas_df.corr results)
        if len(groupby_df.head(1)) > 0:
            # perform correlation in spark, and get the results back in pandas
            df = pd.DataFrame(
                groupby_df.groupby("groupby").apply(spark_phik).toPandas().values,
                columns=selcols,
                index=selcols,
            )
        else:
            df = pd.DataFrame()

        return df


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
