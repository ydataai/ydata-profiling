from pathlib import Path

import pandas as pd

from pandas_profiling import ProfileReport


if __name__ == "__main__":
    df = pd.read_csv(
        "https://github.com/codebrainz/color-names/raw/master/output/colors.csv",
        names=["Code", "Name", "Hex", "R", "G", "B"],
    )
    report = ProfileReport(df, title="Colors")
    report.to_file(Path("colors_report.html"), True)
