from typing import Type

import numpy as np
import pandas as pd
from visions import VisionsBaseType

from pandas_profiling.model.handler import Handler
from pandas_profiling.model.summary_algorithms import (
    describe_categorical_1d,
    describe_counts,
    describe_date_1d,
    describe_file_1d,
    describe_generic,
    describe_image_1d,
    describe_numeric_1d,
    describe_path_1d,
    describe_supported,
    describe_url_1d,
)
from pandas_profiling.model.typeset import (
    URL,
    Boolean,
    Categorical,
    DateTime,
    File,
    Image,
    Numeric,
    Path,
    Unsupported,
)


class BaseSummarizer(Handler):
    """A base summarizer

    Can be used to define custom summarizations
    """

    def summarize(self, series: pd.Series, dtype: Type[VisionsBaseType]) -> dict:
        """

        Returns:
            object:
        """
        _, summary = self.handle(dtype, series, {"type": dtype})
        return summary


class PandasProfilingSummarizer(BaseSummarizer):
    """The default Pandas Profiling summarizer"""

    def __init__(self, typeset, *args, **kwargs):
        summary_map = {
            Unsupported: [
                describe_counts,
                describe_generic,
                describe_supported,
            ],
            Numeric: [
                describe_numeric_1d,
            ],
            DateTime: [
                describe_date_1d,
            ],
            Categorical: [
                describe_categorical_1d,
            ],
            Boolean: [],
            URL: [
                describe_url_1d,
            ],
            Path: [
                describe_path_1d,
            ],
            File: [
                describe_file_1d,
            ],
            Image: [
                describe_image_1d,
            ],
        }
        super().__init__(summary_map, typeset, *args, **kwargs)


def format_summary(summary):
    def fmt(v):
        if isinstance(v, dict):
            return {k: fmt(va) for k, va in v.items()}
        else:
            if isinstance(v, pd.Series):
                return fmt(v.to_dict())
            elif (
                isinstance(v, tuple)
                and len(v) == 2
                and all(isinstance(x, np.ndarray) for x in v)
            ):
                return {"counts": v[0].tolist(), "bin_edges": v[1].tolist()}
            else:
                return v

    summary = {k: fmt(v) for k, v in summary.items()}
    return summary
