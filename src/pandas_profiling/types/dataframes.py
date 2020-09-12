import pandas as pd


class GenericDataFrame(object):
    """
    This class is the abstract layer over the backend data types, and describes the functions and attributes
    that need to be implemented to be a valid backend

    """

    def __init__(self):
        self.df = None
        self.type = None
        self.table_stats = None
        self.variable_stats = None

    def get_columns(self):
        raise NotImplemented("Implementation not found")

    def get_count(self):
        raise NotImplemented("Implementation not found")

    def is_empty(self):
        raise NotImplemented("Implementation not found")

    def get_duplicates(self, subset, keep):
        raise NotImplemented("Implementation not found")

    def dropna(self,subset):
        raise NotImplemented("Implementation not found")

    def groupby(self, columns):
        raise NotImplemented("Implementation not found")

    def get_memory_usage(self, config):
        raise NotImplemented("Implementation not found")

    def __len__(self):
        raise NotImplemented("Implementation not found")

    def __getitem__(self):
        raise NotImplemented("Implementation not found")

    def corr(self, method):
        raise NotImplemented("Implementation not found")

    def get_internal_df(self):
        raise NotImplemented("Implementation not found")


class PandasDataFrame(GenericDataFrame):
    """
    This class is the abstract layer over

    """

    def __init__(self, df):
        super().__init__()
        self.df = df
        self.type = "pandas"
        self.table_stats = None
        self.variable_stats = None

    @staticmethod
    def is_same_type(obj):
        """
        Check if pandas dataframe using isinstance. More pythonic way of checking as opposed to spark type check.
        Possible because its cheap to import pandas dataframe type.

        Args:
            obj: check if object is a spark dataframe

        Returns: True if the __module__ and __name__ of object matches spark dataframe, else false

        """
        print("checking isinstance",isinstance(obj, pd.DataFrame))
        return isinstance(obj, pd.DataFrame)

    def get_columns(self):
        return self.df.columns

    def get_count(self):
        return len(self.df)

    def is_empty(self):
        return self.df.empty

    def get_duplicates(self, subset, keep="First"):
        return self.df.duplicates(subset=subset, keep=keep)

    def dropna(self,subset):
        return self.df.dropna(subset=subset)

    def groupby(self, columns):
        return self.df.groupby(columns)

    def __len__(self):
        return self.get_count()

    def get_memory_usage(self, config):
        return self.df.memory_usage(deep=config["memory_deep"].get(bool)).sum()

    def __getitem__(self):
        return self.df.__getitem__

    def corr(self, method):
        return self.df.corr(method=method)

    def get_internal_df(self):
        """
        This function be deprecated once all functionalities are properly wrapped!!

        Returns:

        """
        return self.df


class SparkDataFrame(GenericDataFrame):
    """
    This class is the abstract layer over

    """

    def __init__(self, df):
        super().__init__()
        self.df = df
        self.type = "spark"
        self.table_stats = None
        self.variable_stats = None

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


def get_implemented_datatypes():
    return (PandasDataFrame, SparkDataFrame)
