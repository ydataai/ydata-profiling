from dataclasses import asdict, is_dataclass
from typing import Any, Callable, Dict, List, Optional, Type, Union

import numpy as np
from pandas_profiling.config import Settings
from pandas_profiling.model.description import BaseDescription
from pandas_profiling.model.description_target import TargetDescription
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
    describe_string_1d,
    describe_supported,
    describe_timeseries_1d,
    describe_url_1d,
)
from visions import VisionsBaseType, VisionsTypeset

import pandas as pd


class BaseSummarizer(Handler):
    """A base summarizer

    Can be used to define custom summarizations
    """

    def summarize(
        self,
        config: Settings,
        series: pd.Series,
        dtype: Type[VisionsBaseType],
        target_description: Optional[TargetDescription] = None,
    ) -> dict:
        """

        Returns:
            object:
        """
        _, _, summary, _ = self.handle(
            str(dtype), config, series, {"type": str(dtype)}, target_description
        )
        return summary


class PandasProfilingSummarizer(BaseSummarizer):
    """The default Pandas Profiling summarizer"""

    def __init__(self, typeset: VisionsTypeset, *args, **kwargs):
        summary_map: Dict[str, List[Callable]] = {
            "Unsupported": [
                describe_counts,
                describe_generic,
                describe_supported,
            ],
            "Numeric": [
                describe_numeric_1d,
            ],
            "DateTime": [
                describe_date_1d,
            ],
            "String": [
                describe_string_1d,
            ],
            "Categorical": [
                describe_categorical_1d,
            ],
            "Boolean": [],
            "URL": [
                describe_url_1d,
            ],
            "Path": [
                describe_path_1d,
            ],
            "File": [
                describe_file_1d,
            ],
            "Image": [
                describe_image_1d,
            ],
            "TimeSeries": [
                describe_timeseries_1d,
            ],
        }
        super().__init__(summary_map, typeset, *args, **kwargs)


def format_summary(summary: Union[BaseDescription, dict]) -> Dict:
    def fmt(v: Any) -> Any:
        if isinstance(v, dict):
            return {k: fmt(va) for k, va in v.items()}
        if isinstance(v, pd.Series):
            return fmt(v.to_dict())
        if (
            isinstance(v, tuple)
            and len(v) == 2
            and all(isinstance(x, np.ndarray) for x in v)
        ):
            return {"counts": v[0].tolist(), "bin_edges": v[1].tolist()}
        if is_dataclass(v):
            v2 = asdict(v)
            return fmt(v2)
        return v

    if isinstance(summary, BaseDescription):
        summary = asdict(summary)

    summary = {k: fmt(v) for k, v in summary.items()}

    return summary
