import warnings
from typing import List

from pyspark.sql.dataframe import DataFrame

from ydata_profiling.config import Settings
from ydata_profiling.model.sample import Sample, get_sample


@get_sample.register
def get_sample_spark(config: Settings, df: DataFrame) -> List[Sample]:
    """Obtains a sample from head and tail of the DataFrame

    Args:
        config: Settings object
        df: the spark DataFrame

    Returns:
        a list of Sample objects
    """
    samples: List[Sample] = []
    if len(df.head(1)) == 0:
        return samples

    n_head = config.samples.head
    if n_head > 0:
        samples.append(
            Sample(id="head", data=df.limit(n_head).toPandas(), name="First rows")
        )

    n_tail = config.samples.tail
    if n_tail > 0:
        warnings.warn(
            "tail sample not implemented for spark. Set config.samples.n_tail to 0 to disable this warning"
        )

    n_random = config.samples.random
    if n_random > 0:
        warnings.warn(
            "random sample not implemented for spark. Set config.samples.n_random to 0 to disable this warning"
        )

    return samples
