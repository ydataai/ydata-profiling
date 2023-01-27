import json
from pathlib import Path

import numpy as np
import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.config import Dataset
from ydata_profiling.utils.cache import cache_file

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

    # Initialize the report
    profile = ProfileReport(df, title="Census Dataset", explorative=True)

    # show column definition
    with open("census_column_definition.json") as f:
        definitions = json.load(f)

    profile.config.dataset = Dataset(
        description='Predict whether income exceeds $50K/yr based on census data. Also known as "Census Income" dataset. Extraction was done by Barry Becker from the 1994 Census database. A set of reasonably clean records was extracted using the following conditions: ((AAGE>16) && (AGI>100) && (AFNLWGT>1)&& (HRSWK>0)). Prediction task is to determine whether a person makes over 50K a year.',
        copyright_year="1996",
        author="Ronny Kohavi and Barry Becker",
        creator="Barry Becker",
        url="https://archive.ics.uci.edu/ml/datasets/adult",
    )
    profile.config.variables.descriptions = definitions

    # Only show the descriptions in the overview
    profile.config.show_variable_description = False

    profile.to_file(Path("./census_report.html"))
