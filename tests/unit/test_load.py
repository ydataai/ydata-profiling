import numpy as np
import pandas as pd
import pytest

from pandas_profiling import ProfileReport


def test_load(Meteorites_df, test_output_dir):

    profile1 = ProfileReport(
        Meteorites_df,
        title="NASA Meteorites",
        samples={"head": 5, "tail": 5},
        minimal=True,
    )

    test_output_path = test_output_dir / "NASA-Meteorites.pp"
    json1 = profile1.to_json()
    profile1.dump(test_output_path)
    _ = profile1.to_html()

    assert test_output_path.exists(), "Output file does not exist"

    profile2 = ProfileReport().load(test_output_path)
    # json1 are compute before dumps, so _description_set should be the same
    assert isinstance(profile2._description_set, dict)

    # profile1 is lazy, html1 are compute after dumps, so report should be None
    assert profile2._report is None

    json2 = profile2.to_json()

    # both profile should generate same output
    assert json1 == json2


def test_load_error():
    df = pd.DataFrame(
        {"a": [1, 2, 3, 1, 1, 1], "b": [1, 2, 3, 4, 5, 6], "c": [1, 2, 3, 4, 5, 6]}
    )
    profile1 = ProfileReport(df, minimal=True)

    data = profile1.dumps()

    # config not match but load_config
    ProfileReport(minimal=False).loads(data, ignore_config=True)

    # config not match
    with pytest.raises(ValueError) as e:
        ProfileReport(minimal=False).loads(data)

    assert (
        str(e.value)
        == 'DataFrame of Config is not match. If you want to overwrite current config, try "load_config=True"'
    )

    # df not match
    with pytest.raises(ValueError) as e:
        ProfileReport(df=df[["a", "b"]][:], minimal=False).loads(
            data, ignore_config=True
        )

    assert (
        str(e.value)
        == 'DataFrame of Config is not match. If you want to overwrite current config, try "load_config=True"'
    )
