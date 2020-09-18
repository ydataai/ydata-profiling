import attr


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

    """

    def __init__(self, series):
        super().__init__(series)
        self.series = series

    @property
    def type(self):
        return self.series.schema.fields[0].dataType

    def fillna(self, fill=None) -> "GenericSeries":
        return self

    @property
    def empty(self) -> bool:
        return self.n_rows == 0

    @property
    def n_rows(self) -> int:
        return self.series.count()
