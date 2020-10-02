from typing import List, Tuple

import numpy as np
import pandas as pd

# annotations allow class methods to return the same class in python < 3.10
from pandas_profiling.model.series_wrappers import (
    GenericSeries,
    PandasSeries,
    Sample,
    SparkSeries,
)
from pandas_profiling.utils.dataframe import rename_index

UNWRAPPED_DATAFRAME_WARNING = """Attempting to pass a pandas dataframe directly into a function that takes a wrapped dataframe, 
                     this function will attempt to automatically wrap this in a pandas_profiling dataframe wrapper,
                     but it is better practice to explicitly wrap it with a backend if calling the
                     function directly : ie. 

                     from pandas_profiling.model.series_wrapper import SparkDataFrame, PandasDataFrame
                     wrapped_df = SparkDataFrame(spark_df)

                     and pass that into the function directly """


class GenericDataFrame(object):
    """
    This class is the abstract layer over the backend data types.
    This enables functions to be called on a dataframe regardless of whether the backend
    is a pandas, spark or (in the future) koalas dataframe
    This class also nicely describes the functions and attributes
    that need to be implemented to support a new backend

    This class should also implement a get_<DATATYPE>_df method (get_pandas_df), which allows you to get the internal
    representation of the data within a singledispatch framework so that you can perform ops specific
    to that datatype within the method

    Some methods inside here return string literals instead of the actual type (ie self.head returns "GenericDataFrame"
    instead of a GenericDataFrame object. This is in accordance to PEP 484 which states that when a type hint contains
     names that have not been defined yet, that definition may be expressed as a string literal, to be resolved later
    https://www.python.org/dev/peps/pep-0484/#id28 .
    From python 3.7 we can use __from__ future import annotations to postpone type evaluation,
    but as there is no plan to drop support for python 3.6 in pandas-profiling this was not a possible solution
    (see PEP 563 for this postponed evaluations strategy https://www.python.org/dev/peps/pep-0563/#abstract)

    """

    def __init__(self):
        # self.df holds the underlying data object
        self.df = None

    @staticmethod
    def validate_same_type(obj) -> bool:
        """
        Check if dataframe provided fits backend

        Args:
            obj: dataframe-like object - check if object is a ___ dataframe

        Returns: True if object fits backend type else false
        """
        raise NotImplemented("Implementation not found")

    @staticmethod
    def preprocess(df):
        """
        This method allows you to modify the dataframe before it is wrapped with a pandas-profiling
        dataframe_wrapper

        Default - do nothing
        For pandas - process the index column properly, because it contains a lot of information
        For spark - spark doesn't really have the idea of an index (maybe partitions comes close?)
        so don't do anything

        Args:
            df: actual dataframe structure

        Returns: preprocess df with some logic before wrapping or do nothing

        """
        raise NotImplementedError("Method not implemented for data type")

    @property
    def columns(self) -> List[str]:
        """
        method to get all the columns in dataframe as a list

        Returns: a list of column names

        """
        raise NotImplemented("Implementation not found")

    @property
    def empty(self) -> bool:
        """
        return True if dataframe is empty, else return false. A dataframe of NaN should not
        evaluate to empty

        Returns: True if dataframe is empty else false

        """
        raise NotImplemented("Implementation not found")

    @property
    def n_rows(self) -> int:
        """
        Get the number of rows in a dataframe as an int

        Returns: number of rows in column

        """
        raise NotImplemented("Implementation not found")

    def get_duplicate_rows_count(self, subset: List[str]) -> int:
        """
        returns the counts of exactly duplicate rows for the subset of columns

        Args:
            subset: subset of rows to consider

        Returns:

        """
        raise NotImplemented("Implementation not found")

    def dropna(self, subset: List[str]) -> "GenericDataFrame":
        """
        returns same dataframe type, but with nan rows dropped for the subset of columns

        Args:
            subset: columns to consider the rows to dropna

        Returns:

        """
        raise NotImplemented("Implementation not found")

    def iteritems(self) -> List[Tuple[str, GenericSeries]]:
        """
        returns name and generic series type

        Returns:

        """
        raise NotImplemented("Implementation not found")

    def groupby_get_n_largest_dups(self, columns: List[str], n: int) -> pd.DataFrame:
        """
        get top n value counts of groupby count function

        Args:
            columns: columns to groupby on
            n: top n value counts to return
            for_duplicates: whether to only keep duplicate rows
        Returns:

        """
        return NotImplemented("Implementation not found")

    def get_memory_usage(self, deep: bool = False) -> pd.Series:
        """
        Get memory usage of dataframe

        Args:
            deep: * For Pandas - interrogating object dtypes for system-level memory consumption

        Returns: A Pandas Series whose index is the original column names and whose values is the
         memory usage of each column in bytes.

        """
        raise NotImplemented("Implementation not found")

    def head(self, n: int):
        """
        Get top n rows of dataframe.
        Only call within singledispatch methods

        Args:
            n: top n rows

        Returns: dataframe with only top n rows

        """
        raise NotImplemented("Implementation not found")

    def tail(self, n):
        """
        Get bottom n rows of dataframe

        Args:
            n: bottom n rows

        Returns: dataframe with only bottom n rows

        """
        raise NotImplemented("Implementation not found")

    def sample(self, n, with_replacement=True):
        """
        Return a sample of dataframe
        Args:
            n: number of rows to sample
            with_replacement: boolean true or false

        Returns:

        """
        raise NotImplemented("Implementation not found")

    def get_sample(self) -> List[Sample]:
        """Obtains a sample from head and tail of the DataFrame

        Returns:
            a list of Sample objects
        """
        raise NotImplementedError("Method not implemented for data type")

    def value_counts(self, column) -> pd.Series:
        """
        Get value counts of a series as a Pandas Series object


        Args:
            column: column to do value_count on

        Returns: an ordered series (descending) where series index is the values to be counted
        and the series values are the counts

        """
        raise NotImplementedError("Method not implemented for data type")

    def __len__(self) -> int:
        """
        Get the number of rows in a dataframe as an int

        Returns: number of rows in column

        """
        raise NotImplemented("Implementation not found")

    def __getitem__(self, key):
        raise NotImplemented("Implementation not found")


class PandasDataFrame(GenericDataFrame):
    """
    This class is the abstract layer for the pandas dataframe.

    It implements the validate_same_type function to check if an obj is a pandas dataframe and can be wrapped.

    It implements the get_pandas_df method to enable singledispatch wrapped functions to
    operate on the internal pandas dataframe without breaking abstraction

    """

    def __init__(self, df):
        super().__init__()
        # self.df holds the underlying data object
        self.df = df

    @staticmethod
    def validate_same_type(obj) -> bool:
        """
        Check if pandas dataframe using isinstance. More pythonic way of checking as opposed to spark type check.
        Possible because its cheap to import pandas dataframe type.

        Args:
            obj: check if object is a spark dataframe

        Returns: True if the __module__ and __name__ of object matches spark dataframe, else false

        """
        return isinstance(obj, pd.DataFrame)

    @staticmethod
    def preprocess(df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the dataframe

        - Appends the index to the dataframe when it contains information
        - Rename the "index" column to "df_index", if exists
        - Convert the DataFrame's columns to str

        Args:
            df: the pandas DataFrame

        Returns:
            The preprocessed DataFrame
        """

        # Treat index as any other column
        if (
            not pd.Index(np.arange(0, len(df))).equals(df.index)
            or df.index.dtype != np.int64
        ):
            df = df.reset_index()

        # Rename reserved column names
        df = rename_index(df)

        # Ensure that columns are strings
        df.columns = df.columns.astype("str")
        return df

    @property
    def columns(self) -> List[str]:
        return self.df.columns

    @property
    def empty(self) -> bool:
        return self.df.empty

    @property
    def n_rows(self) -> int:
        return len(self.df)

    def get_duplicate_rows_count(self, subset) -> int:
        """

        Args:
            subset:
            keep:

        Returns:

        """
        return len(self.df[self.df.duplicated(subset=subset, keep="first")])

    def dropna(self, subset) -> "PandasDataFrame":
        return PandasDataFrame(self.df.dropna(subset=subset))

    def groupby_get_n_largest_dups(self, columns, n) -> pd.DataFrame:
        return (
            self.df[self.df.duplicated(subset=columns, keep=False)]
            .groupby(columns)
            .size()
            .reset_index(name="count")
            .nlargest(n, "count")
        )

    def __len__(self) -> int:
        return self.n_rows

    def get_memory_usage(self, deep=False) -> pd.Series:
        return self.df.memory_usage(deep=deep).sum()

    def __getitem__(self, key):
        return self.df[key]

    def get_pandas_df(self) -> pd.DataFrame:
        return self.df

    def head(self, n) -> pd.DataFrame:
        """
        TODO - should this return a pd.DataFrame or PandasDataFrame?
        Args:
            n:

        Returns:

        """
        return self.df.head(n=n)

    def tail(self, n) -> pd.DataFrame:
        return self.df.tail(n=n)

    def sample(self, n, with_replacement=True) -> pd.DataFrame:
        return self.df.sample(n, with_replacement=with_replacement)

    def value_counts(self, column):
        return self.df[column].value_counts()

    def iteritems(self) -> List[Tuple[str, GenericSeries]]:
        """
        returns name and generic series type

        Returns:

        """
        return [(i[0], PandasSeries(i[1])) for i in self.df.iteritems()]

    def value_counts(self, column):
        return self.df[column].value_counts()

    def iteritems(self) -> List[Tuple[str, GenericSeries]]:
        """
        returns name and generic series type

        Returns:

        """
        return [(i[0], PandasSeries(i[1])) for i in self.df.iteritems()]


class SparkDataFrame(GenericDataFrame):
    """
    A lot of optimisations left to do (persisting, caching etc), but when functionality completed

    """

    def __init__(self, df):
        super().__init__()
        self.df = df

    @staticmethod
    def validate_same_type(obj) -> bool:
        """
        Check if spark dataframe without importing actual spark dataframe class and doing isinstance (too expensive
        to import pyspark class - create more library dependencies for pp)

        Args:
            obj: check if object is a spark dataframe

        Returns: True if the __module__ and __name__ of object matches spark dataframe, else false

        """
        return (
            type(obj).__module__ == "pyspark.sql.dataframe"
            and type(obj).__name__ == "DataFrame"
        )

    @staticmethod
    def get_numeric_types():
        import pyspark.sql.types as T

        # get spark numeric types
        numeric_type_list = [
            T.ByteType,
            T.ShortType,
            T.IntegerType,
            T.LongType,
            T.FloatType,
            T.DoubleType,
            T.DecimalType,
        ]
        return numeric_type_list

    @staticmethod
    def get_categorical_types():
        import pyspark.sql.types as T

        # get spark numeric types
        numeric_type_list = [T.StringType]
        return numeric_type_list

    @staticmethod
    def preprocess(df):
        return df

    @property
    def columns(self) -> List[str]:
        return self.df.columns

    @property
    def schema(self) -> "pyspark.sql.types.StructType":
        return self.df.schema

    @property
    def empty(self) -> bool:
        return self.n_rows == 0

    @property
    def n_rows(self) -> int:
        return self.df.count()

    def get_columns(self) -> List[str]:
        return self.df.columns

    def get_numeric_columns(self) -> List[str]:
        # get columns of df that are numeric as a list
        numeric_columns = []
        for field in self.schema:
            if np.any(
                list(
                    isinstance(field.dataType, d_type)
                    for d_type in self.get_numeric_types()
                )
            ):
                numeric_columns.append(field.name)

        return numeric_columns

    def get_categorical_columns(self) -> List[str]:
        # get columns of df that are numeric as a list
        categorical_columns = []
        for field in self.schema:
            if np.any(
                list(
                    isinstance(field.dataType, d_type)
                    for d_type in self.get_categorical_types()
                )
            ):
                categorical_columns.append(field.name)

        return categorical_columns

    def head(self, n):
        return pd.DataFrame(self.df.head(n), columns=self.columns)

    def sample(self, n, with_replacement=True):
        return self.df.sample(
            withReplacement=with_replacement, frac=n / self.n_rows
        ).toPandas()

    def value_counts(self, column):
        # We can use toPandas here because the output should be somewhat smaller and its
        # only a single row
        # possible optimisation to just use pure spark objects
        df = (
            self.df.groupBy(column).count().orderBy("count", ascending=False).toPandas()
        )
        return pd.Series(df["count"].values, index=df["RAD"].values)

    def __len__(self) -> int:
        return self.n_rows

    def iteritems(self) -> List[Tuple[str, GenericSeries]]:
        """
        returns name and generic series type

        Returns:

        """
        column_list = self.columns
        return [(column, SparkSeries(self.df.select(column))) for column in column_list]

    def get_spark_df(self):
        return self.df

    def dropna(self, subset) -> "SparkDataFrame":
        return SparkDataFrame(self.df.na.drop(subset=subset))

    def get_memory_usage(self, deep):
        return self.df.sample(fraction=0.01).toPandas().memory_usage(deep=deep).sum()

    def groupby_get_n_largest_dups(self, columns, n=None) -> pd.DataFrame:
        import pyspark.sql.functions as F
        from pyspark.sql.functions import array, map_keys, map_values
        from pyspark.sql.types import MapType

        # this is important because dict functions cannot be groupby
        column_type_tuple = list(zip(self.columns, [i.dataType for i in self.schema]))
        converted_dataframe = self.get_spark_df()
        for column, col_type in column_type_tuple:
            if isinstance(col_type, MapType):
                converted_dataframe = converted_dataframe.withColumn(
                    column,
                    array(
                        map_keys(converted_dataframe[column]),
                        map_values(converted_dataframe[column]),
                    ),
                )
        return (
            converted_dataframe.groupBy(self.df.columns)
            .agg(F.count("*"))
            .filter(F.col("count(1)").cast("int") > 1)
            .orderBy("count(1)", ascending=False)
            .limit(n)
            .toPandas()
        )

    def get_duplicate_rows_count(self, subset: List[str]) -> int:
        import pyspark.sql.functions as F

        temp_df = (
            self.df.groupBy(self.df.columns)
            .agg(F.count("*"))
            .select(F.col("count(1)").alias("count").cast("int"))
            .filter(F.col("count") > 1)
            .toPandas()
        )

        return np.sum(temp_df["count"].values)

    def __getitem__(self, key):
        return self.df.select(key)


def get_implemented_datatypes():
    return (PandasDataFrame, SparkDataFrame)
