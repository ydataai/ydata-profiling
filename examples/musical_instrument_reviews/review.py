from pathlib import Path

import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file(
        "reviews_Musical_Instruments_5.json.gz",
        r"http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Musical_Instruments_5.json.gz",
    )

    df = pd.read_json(file_name, compression="gzip", lines=True)

    profile = ProfileReport(
        df, title="Amazon Musical Instrument Review | Profile Report"
    )
    profile.to_file(Path("./review_report.html"))
