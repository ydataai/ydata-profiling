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

if __name__ == "__main__":

    # Download the UCI Bank Marketing Dataset- as seen in examples/bank_marketing_data/banking_data.py
    file_name = cache_zipped_file(
        "bank-full.csv",
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip",
    )

    df = pd.read_csv(file_name, sep=";")

    # The default configuration automatically computes the 'Auto' correlation.
    # You can change the number of bins setting for this calculation as shown below.
    # This setting changes the granularity of the association measure for Numerical-Categorical column pairs.

    profile = ProfileReport(
        df,
        title="Profile Report of the UCI Bank Marketing Dataset",
        config_file="src/ydata_profiling/config_default.yaml",
        correlations={
            "auto": {"n_bins": 8},
        },
    )
    # Saving the data profiling report with the 'auto' correlation matrix to a html file
    profile.to_file(Path("auto_uci_bank_marketing_report.html"))

    # The 'Auto' correlation is also the only correlation computed when no configuration
    # file is specified.

    profile = ProfileReport(
        df,
        title="Profile Report of the UCI Bank Marketing Dataset",
    )

    profile.to_file(Path("auto_no_config_uci_bank_marketing_report.html"))

    # The default configuration only computes the 'Auto' correlation.
    # To deactivate this setting and instead calculate other types of correlations such as Pearson's
    # and Cramer's V we can do the following:

    no_auto_profile = ProfileReport(
        df,
        title="Profile Report of the UCI Bank Marketing Dataset",
        config_file="src/ydata_profiling/config_default.yaml",
        correlations={
            "auto": {"calculate": False},
            "pearson": {"calculate": True},
            "cramers": {"calculate": True},
        },
    )

    # We can then save the data profiling report without the 'auto' correlation matrix to a html file
    no_auto_profile.to_file(Path("no_auto_uci_bank_marketing_report.html"))
