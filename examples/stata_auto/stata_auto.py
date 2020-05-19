from pathlib import Path

import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file("auto2.dta", "http://www.stata-press.com/data/r15/auto2.dta")
    # Suggested by @adamrossnelson
    df = pd.read_stata(file_name)

    # Length left out due to correlation with weight.
    report = ProfileReport(df, title="1978 Automobile dataset", explorative=True)
    report.to_file(Path("stata_auto_report.html"))
