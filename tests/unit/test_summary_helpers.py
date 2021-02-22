import pytest

from pandas_profiling.model.summary_helpers import *


def test_not_implemented():
    with pytest.raises(NotImplementedError):
        get_character_counts(None)

    with pytest.raises(NotImplementedError):
        named_aggregate_summary(None, "")

    with pytest.raises(NotImplementedError):
        length_summary(None, {})


def test_count_duplicate_hash():
    result = count_duplicate_hashes(
        [
            {"hash": "abc"},
            {"hash": "abcd"},
            {"hash": "abcd"},
            {"hash": "asdf"},
            {"hash": "asdf"},
            {"hash": "asdf"},
        ]
    )
    assert result == 3
