from __future__ import annotations

from typing import List, Tuple

import pandas as pd

from pandas_profiling.config import config
# annotations allow class methods to return the same class in python < 3.10
from pandas_profiling.model.series_wrappers import GenericSeries, PandasSeries, Sample


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

    def get_columns(self) -> List[str]:
        """
        method to get all the columns in dataframe as a list

        Returns: a list of column names

        """
        raise NotImplemented("Implementation not found")

    def get_count(self) -> int:
        """
        method to get the number of rows in a dataframe as an int

        Returns: number of rows in column

        """
        raise NotImplemented("Implementation not found")

    def is_empty(self) -> bool:
        """
        return True if dataframe is empty, else return false. A dataframe of NaN should not
        evaluate to empty

        Returns: True if dataframe is empty else false

        """
        raise NotImplemented("Implementation not found")

    def get_duplicates(self, subset: List[str]) -> GenericDataFrame:
        """
        returns only the duplicated rows in the dataframe. Used for the get_duplicates method

        Args:
            subset: subset of rows to consider

        Returns:

        """
        raise NotImplemented("Implementation not found")

    def dropna(self, subset: List[str]) -> GenericDataFrame:
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

    def groupby_get_n_largest(self, columns: List[str], n: int, for_duplicates=True) -> pd.DataFrame:
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

    def head(self, n: int) -> GenericDataFrame:
        """
        Get top n rows of dataframe

        Args:
            n: top n rows

        Returns: dataframe with only top n rows

        """
        raise NotImplemented("Implementation not found")

    def tail(self, n) -> GenericDataFrame:
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
        self.df = df

    @staticmethod
    def validate_same_type(obj):
        """
        Check if pandas dataframe using isinstance. More pythonic way of checking as opposed to spark type check.
        Possible because its cheap to import pandas dataframe type.

        Args:
            obj: check if object is a spark dataframe

        Returns: True if the __module__ and __name__ of object matches spark dataframe, else false

        """
        return isinstance(obj, pd.DataFrame)

    def get_columns(self):
        return self.df.columns

    def get_count(self):
        return len(self.df)

    def is_empty(self):
        return self.df.empty

    def get_duplicates(self, subset, keep="first"):
        return self.df.duplicated(subset=subset, keep=keep)

    def dropna(self, subset):
        return self.df.dropna(subset=subset)

    def groupby_get_n_largest(self, columns, n, for_duplicates=True):
        if for_duplicates:
            return (self.df[self.get_duplicates(subset=columns, keep=False)]
                    .groupby(columns)
                    .size()
                    .reset_index(name="count")
                    .nlargest(n, "count"))
        else:
            return (self.df.groupby(columns)
                    .size()
                    .reset_index(name="count")
                    .nlargest(n, "count"))

    def __len__(self):
        return self.get_count()

    def get_memory_usage(self, deep=False):
        return self.df.memory_usage(deep=deep).sum()

    def __getitem__(self, key):
        return self.df[key]

    def get_pandas_df(self):
        return self.df

    def head(self, n):
        return self.df.head(n=n)

    def tail(self, n):
        return self.df.tail(n=n)

    def sample(self, n, with_replacement=True):
        return self.df.sample(n, with_replacement=with_replacement)

    def get_sample(self) -> list:
        """Obtains a sample from head and tail of the DataFrame

        Returns:
            a list of Sample objects
        """
        samples = []
        n_head = config["samples"]["head"].get(int)
        if n_head > 0:
            samples.append(Sample("head", self.head(n=n_head), "First rows"))

        n_tail = config["samples"]["tail"].get(int)
        if n_tail > 0:
            samples.append(Sample("tail", self.tail(n=n_tail), "Last rows"))

        return samples

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
    def is_same_type(obj):
        """
        Check if spark dataframe without importing actual spark dataframe class and doing isinstance (too expensive
        to import pyspark class - create more library dependencies for pp)

        Args:
            obj: check if object is a spark dataframe

        Returns: True if the __module__ and __name__ of object matches spark dataframe, else false

        """
        return type(obj).__module__ == "pyspark.sql.dataframe" and type(obj).__name__ == "DataFrame"

    def get_count(self):
        return self.df.count()

    def get_columns(self) -> List[str]:
        return self.df.columns

    def head(self, n):
        return pd.DataFrame(self.df.head(10), columns=self.get_columns())

    def sample(self, n, with_replacement=True):
        return self.df.sample(withReplacement=with_replacement, frac=n / self.get_count())

    def value_counts(self, column):
        # We can use toPandas here because the output should be somewhat smaller and its
        # only a single row
        # possible optimisation to just use pure spark objects
        df = self.df.groupBy(column).count().orderBy("count", ascending=False).toPandas()
        return pd.Series(df["count"].values, index=df["RAD"].values)

    def __len__(self):
        return self.get_count()
def get_implemented_datatypes():
    return (PandasDataFrame, SparkDataFrame)
