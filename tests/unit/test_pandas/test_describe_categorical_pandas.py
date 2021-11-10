import pandas as pd
import pytest

from pandas_profiling.model.pandas.describe_categorical_pandas import word_summary_vc

value_counts_w_words = pd.Series(index=["The dog", "is hungry"], data=[2, 1])


def test_word_summary_vc():
    pd.testing.assert_series_equal(
        word_summary_vc(vc=value_counts_w_words)["word_counts"],
        pd.Series(index=["the", "dog", "is", "hungry"], data=[2, 2, 1, 1]),
    )


@pytest.mark.parametrize("stop_words", [["The"], ["the", "a"]])
def test_word_summary_vc_with_stop_words(stop_words):
    pd.testing.assert_series_equal(
        word_summary_vc(vc=value_counts_w_words, stop_words=stop_words)["word_counts"],
        pd.Series(index=["dog", "is", "hungry"], data=[2, 1, 1]),
    )
