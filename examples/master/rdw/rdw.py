import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file(
        "rdw.parquet",
        "https://raw.githubusercontent.com/pandas-profiling/pandas-profiling-data/master/data/rdw.parquet",
    )
    data = pd.read_parquet(file_name)
    for date_column in [
        "Vervaldatum APK",
        "Datum eerste toelating",
        "Datum tenaamstelling",
        "Datum eerste afgifte Nederland",
        "Vervaldatum tachograaf",
    ]:
        data[date_column] = pd.to_datetime(
            data[date_column], format="%Y%m%d", errors="coerce"
        )

    profile = ProfileReport(
        data,
        title="RDW Dataset",
        minimal=True,
    )

    # Interesting, but a bit more expensive:
    # - profile.config.vars.cat.characters = True
    # - profile.config.vars.cat.words = True
    # - profile.config.vars.cat.length = True

    profile.config.vars.url.active = True
    profile.to_file("rdw.html")
