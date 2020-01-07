from pathlib import Path

import pandas as pd

from pandas_profiling import ProfileReport


if __name__ == "__main__":
    df = pd.read_csv(
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    )

    profile = ProfileReport(df, title="Titanic Dataset")
    # profile.to_file(output_file=Path("./titanic_report.html"))
    profile.app()
