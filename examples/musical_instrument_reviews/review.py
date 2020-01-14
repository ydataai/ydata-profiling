from pathlib import Path

import pandas as pd

from pandas_profiling import ProfileReport

if __name__ == "__main__":
    df = pd.read_json(
        r"http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Musical_Instruments_5.json.gz",
        compression="gzip",
        lines=True,
    )

    profile = ProfileReport(
        df, title="Amazon Musical Instrument Review | Profile Report"
    )
    profile.to_file(output_file=Path("./review_report.html"))
