import kaggle
import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.paths import get_data_path

# The dataset in this example is obtained using the `kaggle` api.
# If you haven't done so already, you should set up the api credentials:
# https://github.com/Kaggle/kaggle-api#api-credentials
kaggle.api.authenticate()

# Download the dataset
data_path = get_data_path() / "ieee-fraud-detection"

# https://www.kaggle.com/c/ieee-fraud-detection/
kaggle.api.competition_download_files(
    "ieee-fraud-detection",
    path=str(data_path),
    quiet=False,
)


if not (data_path / "ieee-fraud-detection").exists():
    import zipfile

    with zipfile.ZipFile(data_path / "ieee-fraud-detection.zp", "r") as zip_ref:
        zip_ref.extractall(data_path / "ieee-fraud-detection")


import logging

logging.basicConfig(level=logging.INFO)

df = pd.read_csv(data_path / "ieee-fraud-detection" / "train_transaction.csv")

# Generate the profile report
profile = ProfileReport(
    df,
    title="IEEE-CIS Fraud Detection Dataset",
    explorative=True,
    correlations=dict(
        pearson=dict(calculate=True),
        spearman=dict(calculate=False),
        kendall=dict(calculate=False),
        cramers=dict(calculate=False),
        phi_k=dict(calculate=False),
    ),
    interactions=None,
    missing_diagrams=dict(
        bar=True,
        matrix=False,
        heatmap=False,
        dendrogram=False,
    ),
    html=dict(
        inline=False,
    ),
)

# Save the report
profile.to_file("ieee-fraud-detection.html")
