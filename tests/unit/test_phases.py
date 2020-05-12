import pytest

from pandas_profiling.profile_report import ProfileReport


def test_phases_empty():
    profile = ProfileReport(None)
    with pytest.raises(ValueError) as e:
        profile.to_html()

    assert (
        e.value.args[0]
        == "Can not describe a `lazy` ProfileReport without a DataFrame."
    )
