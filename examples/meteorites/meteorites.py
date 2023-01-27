from pathlib import Path

import numpy as np
import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file(
        "meteorites.csv",
        "https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD",
    )

    # Set a seed for reproducibility
    np.random.seed(7331)

    df = pd.read_csv(file_name)
    # Note: Pandas does not support dates before 1880, so we ignore these for this analysis
    df["year"] = pd.to_datetime(df["year"], errors="coerce")

    # Example: Constant variable
    df["source"] = "NASA"

    # Example: Boolean variable
    df["boolean"] = np.random.choice([True, False], df.shape[0])

    # Example: Mixed with base types
    df["mixed"] = np.random.choice([1, "A"], df.shape[0])

    # Example: unhashable column
    df["unhashable"] = [[1]] * df.shape[0]

    # Example: Highly correlated variables
    df["reclat_city"] = df["reclat"] + np.random.normal(scale=5, size=(len(df)))

    # Example: Duplicate observations
    duplicates_to_add = pd.DataFrame(df.iloc[0:10].copy())

    df = df.append(duplicates_to_add, ignore_index=True)

    logo_string = "data:image/png;base64,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"

    profile = ProfileReport(
        df,
        title="NASA Meteorites",
        html={"style": {"logo": logo_string}},
        correlations={"cramers": {"calculate": False}},
        explorative=True,
    )
    profile.to_file(Path("./meteorites_report.html"))
