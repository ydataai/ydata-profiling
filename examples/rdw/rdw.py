import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file(
        "rdw.parquet",
        "https://raw.githubusercontent.com/pandas-profiling/pandas-profiling-data/master/data/rdw.parquet",
    )
    data = pd.read_parquet(file_name)

    profile = ProfileReport(data, title="RDW Dataset", minimal=True)
    profile.to_file("rdw.html")
