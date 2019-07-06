import pandas as pd
import numpy as np

import pandas_profiling


def test_urls():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/openeventdata/scraper/master/whitelist_urls.csv",
        header=None,
        names=["source", "url", "reach", "language"],
    )

    # Add ~10% missing values
    df = df.mask(np.random.random(df.shape) < 0.1)

    profile = df.profile_report(
        title="DataFrame with URL column", samples={"head": 0, "tail": 0}
    )

    assert "<small>URL</small>" in profile.to_html(), "URL not detected"
    assert (
        "<th>URL</th>\n                <td>1</td>" in profile.to_html()
    ), "URL not detected"
