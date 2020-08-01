import numpy as np
import pandas as pd

import pandas_profiling


def test_urls(get_data_file):
    file_name = get_data_file(
        "whitelist_urls.csv",
        "https://raw.githubusercontent.com/openeventdata/scraper/master/whitelist_urls.csv",
    )

    df = pd.read_csv(
        file_name, header=None, names=["source", "url", "reach", "language"]
    )

    # Add ~10% missing values
    df = df.mask(np.random.random(df.shape) < 0.1)

    profile = df.profile_report(
        title="DataFrame with URL column",
        samples={"head": 0, "tail": 0},
        explorative=True,
    )

    assert "<small>URL</small>" in profile.to_html(), "URL not detected"
    assert "<th>URL</th>" in profile.to_html(), "URL not detected"
