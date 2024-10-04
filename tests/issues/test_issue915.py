"""
Test for issue 915:
https://github.com/ydataai/pandas-profiling/issues/915
Error for series with large integers.
"""
import pandas as pd

from pandas_profiling import ProfileReport


def test_issue915():
    df = pd.DataFrame({"col": pd.Series([716277643516076032 + i for i in range(100)])})
    df_profile = ProfileReport(df)

    def test_with_value(n_extreme_obs):
        """Generate HTML and validate the tabs contain the proper tab titles."""
        df_profile.config.n_extreme_obs = n_extreme_obs
        df_profile.invalidate_cache()

        profile_html = df_profile.to_html()

        assert f">Minimum {n_extreme_obs} values<" in profile_html
        assert f">Maximum {n_extreme_obs} values<" in profile_html

    test_with_value(5)
    test_with_value(100)
    test_with_value(120)
