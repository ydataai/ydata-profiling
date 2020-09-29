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


class GenericSeries(object):
    def __init__(self, series):
        self.series = series

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

    def __init__(self, series):
        super().__init__(series)
        self.series = series

    @property
    def type(self):
        return self.series.schema.fields[0].dataType

    @property
    def name(self):
        return self.series.columns[0]

    @property
    def empty(self) -> bool:
        return self.n_rows == 0

    def fillna(self, fill=None) -> "GenericSeries":
        if fill is not None:
            return SparkSeries(self.series.na.fill(fill))
        else:
            return SparkSeries(self.series.na.fillna())

    @property
    @lru_cache(maxsize=1)
    def n_rows(self) -> int:
        return self.series.count()

    @lru_cache(maxsize=1)
    def value_counts(self, keep_na=True):
        # do not drop NA here
        if keep_na:
            value_counts = self.series.groupBy(self.name).count().toPandas()
        else:
            value_counts = self.series.na.drop().groupBy(self.name).count().toPandas()

        value_counts = (
            value_counts.sort_values("count", ascending=False)
            .set_index(self.name, drop=True)
            .squeeze()
        )
        return value_counts

    @lru_cache(maxsize=1)
    def count_na(self):
        return self.series.count() - self.series.na.drop().count()

    def __len__(self):
        return self.n_rows

    def memory_usage(self, deep):
        """
        Warning! this memory usage is only a sample
        TO-DO can we make this faster or not use a sample?
        """
        return (
            100
            * self.series.sample(fraction=0.01).toPandas().memory_usage(deep=deep).sum()
        )

    def get_spark_series(self):
        return self.series

    def persist(self):
        return self.series.persist()

    def unpersist(self):
        return self.series.unpersist()
