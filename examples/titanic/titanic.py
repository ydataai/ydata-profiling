from pathlib import Path

import pandas as pd
import pandas_profiling

if __name__ == "__main__":
    df = pd.read_csv(
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    )

    profile = df.profile_report(title="Titanic Dataset")
    profile.to_file(output_file=Path("./titanic_report.html"))
