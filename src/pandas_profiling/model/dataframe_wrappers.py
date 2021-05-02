from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from pandas_profiling.config import config as config

# annotations allow class methods to return the same class in python < 3.10
from pandas_profiling.utils.dataframe import rename_index

UNWRAPPED_DATAFRAME_WARNING = """Attempting to pass a pandas dataframe directly into a function that takes a wrapped dataframe, 
                     this function will attempt to automatically wrap this in a pandas_profiling dataframe wrapper,
                     but it is better practice to explicitly wrap it with a backend if calling the
                     function directly : ie. 

                     from pandas_profiling.model.series_wrapper import SparkDataFrame, PandasDataFrame
                     wrapped_df = SparkDataFrame(spark_df)

                     and pass that into the function directly """


class GenericDataFrame(ABC):
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
    @abstractmethod
    def check_if_corresponding_engine(obj) -> bool:
        """
        Check if dataframe provided fits backend

        Args:
            obj: dataframe-like object - check if object is a ___ dataframe

        Returns: True if object fits backend type else false
        """
        pass

    @staticmethod
    @abstractmethod
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
        pass

    @property
    @abstractmethod
    def columns(self) -> List[str]:
        """
        method to get all the columns in dataframe as a list

        Returns: a list of column names

        """
        pass

    @property
    @abstractmethod
    def empty(self) -> bool:
        """
        return True if dataframe is empty, else return false. A dataframe of NaN should not
        evaluate to empty

        Returns: True if dataframe is empty else false

        """
        pass

    @abstractmethod
    def get_duplicate_rows_count(self, subset: List[str]) -> int:
        """
        returns the counts of exactly duplicate rows for the subset of columns

        Args:
            subset: subset of rows to consider

        Returns:

        """
        pass

    @abstractmethod
    def groupby_get_n_largest_dups(self, columns: List[str], n: int) -> pd.DataFrame:
        """
        get top n value counts of groupby count function

        Args:
            columns: columns to groupby on
            n: top n value counts to return
            for_duplicates: whether to only keep duplicate rows
        Returns:

        """
        pass

    @abstractmethod
    def get_memory_usage(self, deep: bool = False) -> pd.Series:
        """
        Get memory usage of dataframe

        Args:
            deep: * For Pandas - interrogating object dtypes for system-level memory consumption

        Returns: A Pandas Series whose index is the original column names and whose values is the
         memory usage of each column in bytes.

        """
        pass

    @abstractmethod
    def head(self, n: int):
        """
        Get top n rows of dataframe.
        Only call within singledispatch methods

        Args:
            n: top n rows

        Returns: dataframe with only top n rows

        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """
        Get the number of rows in a dataframe as an int

        Returns: number of rows in column

        """
        pass

    @abstractmethod
    def __getitem__(self, key):
        pass


class PandasDataFrame(GenericDataFrame):
    """
    This class is the abstract layer for the pandas dataframe.

    It implements the check_if_corresponding_engine function to check if an obj is a pandas dataframe and can be wrapped.

    It implements the get_pandas_df method to enable singledispatch wrapped functions to
    operate on the internal pandas dataframe without breaking abstraction

    """

    engine = "pandas"

    def __init__(self, df):
        super().__init__()
        # self.df holds the underlying data object
        self.df = df
        self.n_rows = len(self.df)

    @staticmethod
    def check_if_corresponding_engine(obj) -> bool:
        """
        Check if pandas dataframe using isinstance. More pythonic way of checking as opposed to spark type check.

        Args:
            obj: check if object is a pandas dataframe

        Returns: True if the __module__ and __name__ of object matches pandas dataframe, else false
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

    def groupby_get_n_largest_dups(
        self, supported_columns, n_head
    ) -> Tuple[Dict[str, Any], Optional[pd.DataFrame]]:

        metrics: Dict[str, Any] = {}
        if n_head > 0:
            if supported_columns and len(self.df) > 0:
                duplicates_key = config["duplicates"]["key"].get(str)
                if duplicates_key in self.df.columns:
                    raise ValueError(
                        f"Duplicates key ({duplicates_key}) may not be part of the DataFrame. Either change the "
                        f" column name in the DataFrame or change the 'duplicates.key' parameter."
                    )

                duplicated_rows = self.df.duplicated(
                    subset=supported_columns, keep=False
                )
                duplicated_rows = (
                    self.df[duplicated_rows]
                    .groupby(supported_columns)
                    .size()
                    .reset_index(name=duplicates_key)
                )

                metrics["n_duplicates"] = len(duplicated_rows[duplicates_key])
                metrics["p_duplicates"] = metrics["n_duplicates"] / len(self.df)

                return (
                    metrics,
                    duplicated_rows.nlargest(n_head, duplicates_key),
                )
            else:
                metrics["n_duplicates"] = 0
                metrics["p_duplicates"] = 0.0
                return metrics, None
        else:
            return metrics, None

    def __len__(self) -> int:
        return self.n_rows

    def get_memory_usage(self, deep: bool = False) -> pd.Series:
        return self.df.memory_usage(deep=deep).sum()

    def __getitem__(self, key):
        return self.df[key]

    def get_pandas_df(self) -> pd.DataFrame:
        return self.df

    def head(self, n) -> pd.DataFrame:
        """
        return top n rows of PandasDataFrame

        Args:
            n: number of rows to return

        Returns: pd.DataFrame with top n rows
        """
        return self.df.head(n=n)

    def tail(self, n) -> pd.DataFrame:
        """
        this function is not mandatory - it is only called for the pandas backend in sample.py.
        We do not have something similar for spark backend

        Args:
            n: number of tail rows to get

        Returns: pandas dataframe with n tail rows

        """
        return self.df.tail(n=n)

    def sample(self, n, with_replacement=True) -> pd.DataFrame:
        return self.df.sample(n, with_replacement=with_replacement)

    def value_counts(self, column):
        return self.df[column].value_counts()

    def iteritems(self) -> List[Tuple[str, pd.Series]]:
        """
        returns name and generic series type

        Returns: list of (series name,series object) tuples
        """
        return self.df.iteritems()


class SparkDataFrame(GenericDataFrame):
    """
    This class is the abstract layer for the Spark dataframe.

    It implements the check_if_corresponding_engine function to check if an obj is a pandas dataframe and can be wrapped.

    It implements the get_spark_dataframe method to enable singledispatch wrapped and spark-type aware functions to
    operate on the internal spark dataframe without breaking abstraction

    Note that spark commands must NEVER be called during the pandas workflow of profiling, as that means
    people would need to install pyspark to profile pandas dataframes which is very bad design.
    """

    engine = "spark"

    def __init__(self, df, persist=True):
        super().__init__()
        self.df = df
        self.persist_bool: bool = persist
        self.persist()

        # get all columns in df that are numeric as pearson works only on numeric columns
        numeric_columns = self.get_numeric_columns()

        if len(numeric_columns) > 1:
            from pyspark.ml.feature import VectorAssembler

            # Can't compute correlations with 1 or less columns
            # assemble all numeric columns into a vector
            assembler = VectorAssembler(inputCols=numeric_columns, outputCol="features")
            output_df = assembler.transform(self.df)
            self.as_vector = output_df

        self.n_rows: int = self.df.count()

        # here we generate a sample in pandas, so we can keep calling this sample
        sample = config["spark"]["sample"].get(int)
        if self.n_rows < sample:
            self.sample: pd.DataFrame = self.df.toPandas()
        else:
            percentage = sample / self.n_rows
            self.sample: pd.DataFrame = self.df.sample(fraction=percentage).toPandas()

    @staticmethod
    def check_if_corresponding_engine(obj) -> bool:
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
    def preprocess(df):
        return df

    @property
    def columns(self) -> List[str]:
        return self.df.columns

    @property
    def schema(self):
        return self.df.schema

    @property
    def empty(self) -> bool:
        return self.n_rows == 0

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

    def head(self, n):
        return pd.DataFrame(self.df.head(n), columns=self.columns)

    def __len__(self) -> int:
        return self.n_rows

    def get_spark_df(self):
        return self.df

    @lru_cache()
    def get_memory_usage(self, deep: bool = False):
        return 1000 * self.sample.memory_usage(deep=deep)

    def groupby_get_n_largest_dups(
        self, columns, n=None
    ) -> Tuple[Dict[str, Any], Optional[pd.DataFrame]]:
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

        metrics: Dict[str, Any] = {}

        # TODO COMPUTE THIS PROPERLY
        # metrics["n_duplicates"] = len(duplicated_rows[duplicates_key])

        duplicated_df = (
            converted_dataframe.groupBy(self.df.columns)
            .count()
            .withColumn("count", F.col("count").cast("int"))
            .filter(F.col("count") > 1)
        )

        metrics["n_duplicates"] = duplicated_df.count()
        metrics["p_duplicates"] = metrics["n_duplicates"] / self.n_rows

        return metrics, (
            duplicated_df.orderBy("count", ascending=False).limit(n).toPandas()
        )

    def get_duplicate_rows_count(self, subset: List[str]) -> int:
        """
        Reference commands to understand this code
        number of unique rows -> self.dropna.distinct().count()
        number of deduplicated rows - > self.dropna.dropDuplicates().count()
        thus to get number of duplicate rows, we take number of deduplicated rows - number of unique rows
        """
        num_duplicates = self.df.dropDuplicates().count() - self.df.distinct().count()

        return num_duplicates

    def nan_counts(self):
        """
        Only in spark implementation, because pandas already has isnull().sum()
        we use .squeeze(axis="index") to ensure that it doesn't become a scalar

        Use this function to get a count of all the nan values.
        Used in pandas_profiling.visualisation.missing function

        Returns: Pandas Series of NaN counts in each column

        """
        import pyspark.sql.functions as F

        return (
            self.df.agg(
                *[F.count(F.when(F.isnull(c), c)).alias(c) for c in self.df.columns]
            )
            .toPandas()
            .squeeze(axis="index")
        )

    def persist(self):
        """
        this function is the adaptor to call a persist on the underlying dataframe.

        self.persist_bool can be set as false to always prevent any persist from happening

        Returns: None, but persists the underlying spark dataframe within the SparkDataFrame object

        """
        if self.persist_bool:
            self.df.persist()

    def unpersist(self):
        """
        this function is the adaptor to call a unpersist on the underlying dataframe

        Returns: None, but unpersists the underlying spark dataframe within the SparkDataFrame object

        """
        if self.persist_bool:
            self.df.unpersist()

    def __getitem__(self, key):
        return self.df.select(key)


def get_implemented_engines():
    """
    This is a helper function to enumerate all the implemented engines

    Returns: list of class objects of implemented compute engines

    """
    return [PandasDataFrame, SparkDataFrame]


def get_appropriate_wrapper(df):
    """
    Wrap data type with proper engine from get_implemented_engines

    This function also updates config with the respective engine based on input.

    Raises NotImplementedError if no valid engine found

    Args:
        df: the dataframe to be profiled - currently Spark and Pandas dataframes are supported

    Returns: An implementation of the GenericDataFrame object, currently either SparkDataFrame or PandasDataFrame

    """
    implemented_engines = get_implemented_engines()
    for engine in implemented_engines:
        if engine.check_if_corresponding_engine(df):
            # set config with engine
            config.set_kwargs({"engine": engine})
            return engine

    raise NotImplementedError(
        f"""Datatype is currently not supported. Support data types are {implemented_engines}"""
    )
