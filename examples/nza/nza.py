from pathlib import Path

import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file(
        "nza_01_DBC.csv", "https://www.opendisdata.nl/download/csv/01_DBC.csv"
    )

    df = pd.read_csv(file_name, low_memory=False)
    df["JAAR"] = pd.to_datetime(df["JAAR"], format="%Y")

    profile = ProfileReport(df, title="NZa")
    profile.to_file(output_file=Path("./nza_report.html"))
