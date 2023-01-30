from pathlib import Path

import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_zipped_file

"""
The "Auto" correlation is an interpretable pairwise column metric of the following mapping:

- Variable_type-Variable_type : Method, **Range** 
- Categorical-Categorical     : Cramer's V, **[0,1]**
- Numerical-Categorical       : Cramer's V, **[0,1]** (using a discretized numerical column)
- Numerical-Numerical         : Spearman's Rho, **[-1,1]**

"""

# Download the UCI Bank Marketing Dataset- as seen in examples/bank_marketing_data/banking_data.py
file_name = cache_zipped_file(
    "bank-full.csv",
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip",
)

df = pd.read_csv(file_name, sep=";")

profile = ProfileReport(
    df, title="Profile Report of the UCI Bank Marketing Dataset", explorative=True
)


# The simplest way to change the number of bins is either through your script or notebook.
# This changes the granularity of the association measure for Numerical-Categorical column pairs.
profile.config.correlations["auto"].n_bins = 8


# The 'auto' correlation matrix is displayed with the other correlation matrices in the report.
profile.to_file(Path("uci_bank_marketing_report.html"))
