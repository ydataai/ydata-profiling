from functools import reduce
from typing import Type

import pandas as pd
from visions import VisionsBaseType

from pandas_profiling.model.summary_algorithms import (
    describe_categorical_1d,
    describe_counts,
    describe_date_1d,
    describe_file_1d,
    describe_image_1d,
    describe_numeric_1d,
    describe_path_1d,
    describe_supported,
    describe_unsupported,
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


def compose(functions):
    """
    Compose a sequence of functions
    :param functions: sequence of functions
    :return: combined functions, e.g. [f(x), g(x)] -> g(f(x))
    """
    return reduce(lambda f, g: lambda *x: f(*g(*x)), reversed(functions), lambda *x: x)


class BaseSummarizer:
    def __init__(self, summary_map, *args, **kwargs):
        self.summary_map = summary_map

    def summarize(self, series: pd.Series, dtype: Type[VisionsBaseType]) -> dict:
        """

        Returns:
            object: 
        """
        # TODO: follow inference path
        summarizer_func = compose(self.summary_map.get(dtype, []))
        _, summary = summarizer_func(series, {"type": dtype})
        return summary


class PandasProfilingSummarizer(BaseSummarizer):
    def __init__(self, *args, **kwargs):
        compression_map = {
            Unsupported: [describe_counts, describe_unsupported, describe_supported],
            Numeric: [
                describe_counts,
                describe_unsupported,
                describe_supported,
                describe_numeric_1d,
            ],
            DateTime: [
                describe_counts,
                describe_unsupported,
                describe_supported,
                describe_date_1d,
            ],
            Categorical: [
                describe_counts,
                describe_unsupported,
                describe_supported,
                describe_categorical_1d,
            ],
            Boolean: [describe_counts, describe_unsupported, describe_supported],
            URL: [
                describe_counts,
                describe_unsupported,
                describe_supported,
                describe_categorical_1d,
                describe_url_1d,
            ],
            Path: [
                describe_counts,
                describe_unsupported,
                describe_supported,
                describe_categorical_1d,
                describe_path_1d,
            ],
            File: [
                describe_counts,
                describe_unsupported,
                describe_supported,
                describe_categorical_1d,
                describe_path_1d,
                describe_file_1d,
            ],
            Image: [
                describe_counts,
                describe_unsupported,
                describe_supported,
                describe_categorical_1d,
                describe_path_1d,
                describe_file_1d,
                describe_image_1d,
            ],
            # Count? Float? etc.
            # TimeDelta: [],
            # Complex: [describe_counts, describe_supported, describe_complex_1d],
        }
        super().__init__(compression_map, *args, **kwargs)


# Or on summary?
# TODO: move
def format_summary(summary):
    def fmt(v):
        if isinstance(v, pd.Series):
            return v.to_dict()
        elif isinstance(v, tuple) and len(v) == 2:
            return {"counts": v[0].tolist(), "bin_edges": v[1].tolist()}
        else:
            return v

    summary = {k: fmt(v) for k, v in summary.items()}
    return summary


if __name__ == "__main__":
    pps = PandasProfilingSummarizer()

    print(format_summary(pps.summarize(pd.Series([1, 2, 3, 4, 5]), Unsupported)))
    print(format_summary(pps.summarize(pd.Series([1, 2, 3, 4, 5]), Numeric)))
    print(
        format_summary(
            pps.summarize(
                pd.Series(pd.date_range(start="1/1/2018", end="1/08/2018")), DateTime
            )
        )
    )
    print(format_summary(pps.summarize(pd.Series(["abc", "abc", "abba"]), Categorical)))
    print(format_summary(pps.summarize(pd.Series(["https://www.example.com"]), URL)))
    print(
        format_summary(
            pps.summarize(
                pd.Series(
                    [
                        r"C:\Users\Cees Closed\Documents\code\pandas-profiling\src\pandas_profiling\model\typeset.py"
                    ]
                ),
                Path,
            )
        )
    )
    print(
        format_summary(
            pps.summarize(
                pd.Series(
                    [
                        r"C:\Users\Cees Closed\Documents\code\pandas-profiling\src\pandas_profiling\model\typeset.py"
                    ]
                ),
                File,
            )
        )
    )
    print(
        format_summary(
            pps.summarize(
                pd.Series(
                    [
                        r"C:\Users\Cees Closed\Documents\code\pandas-profiling\docsrc\assets\lambda-labs.png"
                    ]
                ),
                Image,
            )
        )
    )
    print(
        format_summary(
            pps.summarize(pd.Series([True, False, True, False, False]), Boolean)
        )
    )
