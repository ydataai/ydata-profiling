"""
Test for issue 864:
https://github.com/ydataai/ydata-profiling/issues/

Validate Extreme Values sub-tabs state the correct number of extreme values shown.
"""
import random

import pandas as pd

from ydata_profiling import ProfileReport


def test_issue864():
    def random_list(n):
        return [random.randrange(0, 100) for _ in range(0, n)]

    df = pd.DataFrame({"a": random_list(30)})

    profile = ProfileReport(df)

    def test_with_value(n_extreme_obs):
        """Generate HTML and validate the tabs contain the proper tab titles."""
        profile.config.n_extreme_obs = n_extreme_obs
        profile.invalidate_cache()

        html = profile.to_html()

        assert f">Minimum {n_extreme_obs} values<" in html
        assert f">Maximum {n_extreme_obs} values<" in html

    test_with_value(5)
    test_with_value(10)
    test_with_value(12)
