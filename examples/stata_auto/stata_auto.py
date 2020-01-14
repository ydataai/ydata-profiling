from pathlib import Path

import pandas as pd
from pandas_profiling import ProfileReport


if __name__ == "__main__":
    # Suggested by @adamrossnelson
    df = pd.read_stata("http://www.stata-press.com/data/r15/auto2.dta")

    # Length left out due to correlation with weight.
    report = ProfileReport(df, title="1978 Automobile dataset")
    report.to_file(Path("stata_auto_report.html"))
