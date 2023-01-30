from pathlib import Path

import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file(
        "chicago_employees.csv",
        "https://data.cityofchicago.org/api/views/xzkq-xp2w/rows.csv?accessType=DOWNLOAD",
    )

    df = pd.read_csv(file_name)

    profile = ProfileReport(df, title="Chicago Employees", explorative=True)
    profile.to_file(Path("./chicago_employees_report.html"))
