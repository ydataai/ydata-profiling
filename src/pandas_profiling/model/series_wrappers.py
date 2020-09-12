from abc import ABC, abstractmethod
from functools import lru_cache

import attr

UNWRAPPED_SERIES_WARNING = """Attempting to pass a pandas series directly into a function that takes a wrapped series, 
                     this function will attempt to automatically wrap this in a pandas_profiling series wrapper,
                     but it is better practice to explicitly wrap it with a backend if calling the
                     function directly : ie. 
                     
                     from pandas_profiling.model.series_wrapper import SparkSeries, PandasSeries
                     wrapped_df = SparkSeries(spark_df)
                     
                     and pass that into the function directly """


@attr.s
class Sample(object):
    id = attr.ib()
    data = attr.ib()
    name = attr.ib()
    caption = attr.ib(default=None)


class GenericSeries(ABC):
    def __init__(self, series):
        self.series = series

    @abstractmethod
    def fillna(self, fill=None) -> "GenericSeries":
        raise NotImplementedError("Method not implemented for data type")


class PandasSeries(GenericSeries):
    """
    This class is the abstract layer over

    """

    def __init__(self, series):
        super().__init__(series)
        self.series = series

    def fillna(self, fill=None) -> "PandasSeries":
        if fill is not None:
            return PandasSeries(self.series.fillna(fill))
        else:
            return PandasSeries(self.series.fillna())


class SparkSeries(GenericSeries):
    """
    A lot of optimisations left to do (persisting, caching etc), but when functionality completed

    TO-DO Also SparkSeries does a lot more than PandasSeries now, likely abstraction issue
    TO-DO .na.drop() is called multiple times, can we optimise this?
    """

    def __init__(self, series, persist=True):
        super().__init__(series)
        from pyspark.sql.functions import array, map_keys, map_values
        from pyspark.sql.types import MapType

        # if series type is dict, handle that separately
        if isinstance(self.series.schema[0].dataType, MapType):
            series= series.select(array(map_keys(series[self.name]), map_values(series[self.name])).alias(self.name))
        self.series = series
        self.persist_bool = persist
        series_without_na = self.series.na.drop()
        series_without_na.persist()
        self.dropna = series_without_na

    @property
    def type(self):
        return self.series.schema.fields[0].dataType

    @property
    def name(self):
        return self.series.columns[0]

    @property
    def empty(self) -> bool:
        return self.n_rows == 0

    def unpersist_series_without_na(self):
        """
        Useful wrapper for getting the internal data series but with NAs dropped
        Returns: internal spark series without nans

        """
        self.dropna.unpersist()

    def fillna(self, fill=None) -> "SparkSeries":
        if fill is not None:
            return SparkSeries(self.series.na.fill(fill), persist=self.persist_bool)
        else:
            return SparkSeries(self.series.na.fillna(), persist=self.persist_bool)

    @property
    @lru_cache()
    def n_rows(self) -> int:
        return self.series.count()

    def value_counts(self):
        """

        Args:
            n: by default, get only 1000

        Returns:

        """

        from pyspark.sql.functions import array, map_keys, map_values
        from pyspark.sql.types import MapType

        # if series type is dict, handle that separately
        if isinstance(self.series.schema[0].dataType, MapType):
            new_df = self.dropna.groupby(
                map_keys(self.series[self.name]).alias("key"),
                map_values(self.series[self.name]).alias("value"),
            ).count()
            value_counts = (
                new_df.withColumn(self.name, array(new_df["key"], new_df["value"]))
                .select(self.name, "count")
                .orderBy("count", ascending=False)
            )
        else:
            value_counts = self.dropna.groupBy(self.name).count()
        value_counts.persist()
        return value_counts

    @lru_cache()
    def count_na(self):
        return self.n_rows - self.dropna.count()

    def __len__(self):
        return self.n_rows

    def memory_usage(self, deep):
        """
        Warning! this memory usage is only a sample
        TO-DO can we make this faster or not use a sample?
        """
        sample = self.n_rows ** (1 / 3)
        percentage = sample / self.n_rows
        inverse_percentage = 1 / percentage
        return (
            inverse_percentage
            * self.series.sample(fraction=percentage)
            .toPandas()
            .memory_usage(deep=deep)
            .sum()
        )

    def get_spark_series(self):
        return self.series

    def persist(self):
        if self.persist_bool:
            self.series.persist()

    def unpersist(self):
        if self.persist_bool:
            self.series.unpersist()

    def distinct(self):
        return self.dropna.distinct().count()

    def unique(self):
        return self.dropna.dropDuplicates().count()
