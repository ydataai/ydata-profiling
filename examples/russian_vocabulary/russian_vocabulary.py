from pathlib import Path

import pandas as pd

from pandas_profiling import ProfileReport


if __name__ == "__main__":
    df = pd.read_csv(
        r"https://raw.githubusercontent.com/aliceriot/russian-vocab/master/words.csv",
        names=["russian", "english", "part of speech"],
    )
    profile = ProfileReport(
        df, title="Russian 1000 most occurring words | Profile Report"
    )
    profile.to_file(output_file=Path("./russian_vocabulary.html"))
