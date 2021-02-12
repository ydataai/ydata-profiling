import sys
from unittest.mock import Mock

import pandas as pd
import pytest

from pandas_profiling import ProfileReport


@pytest.fixture
def df():
    return pd.DataFrame({"num": [1, 2, 3, 4, 5]})


def test_to_expectation_suite_raises(df):
    report = ProfileReport(df)
    with pytest.raises(ImportError):
        report.to_expectation_suite()


def test_to_expectation_suite(df):
    mod = Mock()
    context = Mock()
    sys.modules["great_expectations"] = mod

    report = ProfileReport(df)
    _ = report.to_expectation_suite(
        suite_name="titanic_expectations",
        data_context=context,
        save_suite=False,
        run_validation=False,
        build_data_docs=False,
    )

    mod.data_context.DataContext.assert_not_called()
    context.create_expectation_suite.assert_called_once_with(
        "titanic_expectations", overwrite_existing=True
    )
    mod.dataset.PandasDataset.assert_called_once()

    _ = report.to_expectation_suite(
        suite_name="titanic_expectations",
        save_suite=False,
        run_validation=False,
        build_data_docs=False,
    )
    mod.data_context.DataContext.assert_called_once()
