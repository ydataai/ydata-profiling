from pathlib import Path

import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file(
        "colors.csv",
        "https://github.com/codebrainz/color-names/raw/master/output/colors.csv",
    )

    df = pd.read_csv(file_name, names=["Code", "Name", "Hex", "R", "G", "B"])
    report = ProfileReport(df, title="Colors", explorative=True)
    report.to_file(Path("colors_report.html"))
