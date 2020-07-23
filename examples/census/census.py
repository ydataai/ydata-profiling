from pathlib import Path

import os
import sys
import json
import numpy as np
import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file(
        "census_train.csv",
        "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
    )

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

    # Get filepath
    filepath, _ = dirname, filename = os.path.split(os.path.abspath(__file__))
    profile = ProfileReport(
        df,
        title="Census Dataset",
        explorative=True,
        definition_file=f'{filepath}/census_column_definition.json' # show column definition in overview
    )

    # show column definition in variables
    definitions= json.load(open(f'{filepath}/census_column_definition.json', 'r'))
    profile.set_variable('variables.descriptions', definitions)

    profile.to_file(Path("./census_report.html"))
