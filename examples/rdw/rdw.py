import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file(
        "rdw.parquet",
        "https://github.com/pandas-profiling/pandas-profiling-data/raw/master/data/rdw.parquet",
    )
    data = pd.read_parquet(file_name)

    profile = ProfileReport(
        data, title="RDW Dataset", minimal=True, vars={"url": {"active": True}}
    )
    profile.to_file("rdw.html")
