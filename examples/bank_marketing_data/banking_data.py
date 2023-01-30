# As featured on this Google Cloud Platform page:
# https://cloud.google.com/solutions/building-a-propensity-model-for-financial-services-on-gcp
from pathlib import Path

import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_zipped_file

if __name__ == "__main__":
    file_name = cache_zipped_file(
        "bank-full.csv",
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip",
    )

    # Download the UCI Bank Marketing Dataset
    df = pd.read_csv(file_name, sep=";")

    profile = ProfileReport(
        df, title="Profile Report of the UCI Bank Marketing Dataset", explorative=True
    )
    profile.to_file(Path("uci_bank_marketing_report.html"))
