from pathlib import Path

import pandas as pd

import pandas_profiling

if __name__ == "__main__":
    df = pd.read_csv(
        "https://www.opendisdata.nl/download/csv/01_DBC.csv", low_memory=False
    )
    df["JAAR"] = pd.to_datetime(df["JAAR"], format="%Y")

    # Use an intermediate date as thershold to split the samples
    df["SAMPLE_SPLIT"] =  df["JAAR"] > "2015-01-01"

    profile = df.profile_report(title="NZa", 
                                col_split="SAMPLE_SPLIT")
    profile.to_file(output_file=Path("./nza_report_psi.html"))
