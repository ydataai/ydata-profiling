from functools import lru_cache

import attr


@attr.s
class Sample:
    id = attr.ib()
    data = attr.ib()
    name = attr.ib()
    caption = attr.ib(default=None)


class SparkSeries:
    """
    A lot of optimisations left to do (persisting, caching etc), but when functionality completed
    """

    def __init__(self, series, persist=True):
        from pyspark.sql.functions import array, map_keys, map_values
        from pyspark.sql.types import MapType

        self.series = series
        # if series type is dict, handle that separately
        if isinstance(series.schema[0].dataType, MapType):
            self.series = series.select(
                array(map_keys(series[self.name]), map_values(series[self.name])).alias(
                    self.name
                )
            )

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
        TODO: can we make this faster or not use a sample?
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
