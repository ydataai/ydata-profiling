from pathlib import Path

import pandas as pd
import numpy as np
import requests

from pandas_profiling import ProfileReport


if __name__ == "__main__":
    file_name = Path("rows.csv")
    if not file_name.exists():
        data = requests.get(
            "https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD"
        )
        file_name.write_bytes(data.content)

    df = pd.read_csv(file_name)
    # Note: Pandas does not support dates before 1880, so we ignore these for this analysis
    df["year"] = pd.to_datetime(df["year"], errors="coerce")

    # Example: Constant variable
    df["source"] = "NASA"

    # Example: Boolean variable
    df["boolean"] = np.random.choice([True, False], df.shape[0])

    # Example: Mixed with base types
    df["mixed"] = np.random.choice([1, "A"], df.shape[0])

    # Example: Highly correlated variables
    df["reclat_city"] = df["reclat"] + np.random.normal(scale=5, size=(len(df)))

    # Example: Duplicate observations
    duplicates_to_add = pd.DataFrame(df.iloc[0:10])
    duplicates_to_add[u"name"] = duplicates_to_add[u"name"] + " copy"

    df = df.append(duplicates_to_add, ignore_index=True)

    profile = ProfileReport(
        df, title="NASA Meteorites", correlation_overrides=["recclass"]
    )
    profile.to_file(output_file=Path("./meteorites_report.html"))
