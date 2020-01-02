from pathlib import Path

import pandas as pd
import numpy as np
import requests

from pandas_profiling import ProfileReport

if __name__ == "__main__":
    file_name = Path("census_train.csv")
    if not file_name.exists():
        data = requests.get(
            "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
        )
        file_name.write_bytes(data.content)

    # Names based on https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.names
    df = pd.read_csv(
        file_name,
        header=None,
        index_col=False,
        names=[
            "age",
            "workclass",
            "fnlwgt",
            "education",
            "education-num",
            "marital-status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "capital-gain",
            "capital-loss",
            "hours-per-week",
            "native-country",
        ],
    )

    # Prepare missing values
    df = df.replace("\\?", np.nan, regex=True)

    profile = ProfileReport(df, title="Census Dataset")
    profile.to_file(output_file=Path("./census_report.html"))
