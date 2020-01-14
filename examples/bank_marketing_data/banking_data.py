# As featured on this Google Cloud Platform page:
# https://cloud.google.com/solutions/building-a-propensity-model-for-financial-services-on-gcp


import pandas as pd

from pandas_profiling import ProfileReport


if __name__ == "__main__":
    # Download the UCI Bank Marketing Dataset
    df = pd.read_csv(
        "https://storage.googleapis.com/erwinh-public-data/bankingdata/bank-full.csv",
        sep=";",
    )

    profile = ProfileReport(
        df, title="Profile Report of the UCI Bank Marketing Dataset"
    )
    profile.to_file("uci_bank_marketing_report.html")
