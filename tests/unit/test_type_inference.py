import numpy as np
import pandas as pd
import pytest

from pandas_profiling.model.handler import default_handler
from pandas_profiling.model.typeset import Bool, Numeric, ProfilingTypeSet


@pytest.fixture()
def handler():
    return default_handler()


def test_numeric_with_inf(handler):
    s = pd.Series([1, 2, 3, 6, np.inf])
    assert handler.typeset.infer_type(s) == Numeric


def test_bool(handler):
    s = pd.Series([True, True, True, False, False, False], dtype=bool)
    assert s in Bool
    assert s not in Numeric
    assert handler.typeset.infer_type(s).__name__ == "Bool"


@pytest.mark.parametrize(
    "name,values",
    [
        ("booleans_type", [False, True, True]),
        ("booleans_type_nan", [False, True, np.nan]),
        ("integers", [1, 0, 0]),
        ("integers_nan", [1, 0, np.nan]),
        ("str_yes_no", ["Y", "N", "Y"]),
        ("str_yes_no_mixed", ["Y", "n", "y"]),
        ("str_yes_no_nana", ["Y", "N", np.nan]),
        ("str_true_false", ["True", "False", "False"]),
        ("str_true_false_nan", ["True", "False", np.nan]),
    ],
)
def test_bool_inference(handler, name, values):
    assert handler.typeset.infer_type(pd.Series(values, name=name)).__name__ == "Bool"


def test_type_inference(get_data_file, handler):
    file_name = get_data_file(
        "pandas_profiling_bug.txt",
        "https://github.com/pandas-profiling/pandas-profiling/files/2386812/pandas_profiling_bug.txt",
    )
    df = pd.read_csv(file_name)

    typset = ProfilingTypeSet()
    print(typset.detect_type(df["device_isMobile"]))

    print(handler.typeset.infer_type(df["device_isMobile"]))
