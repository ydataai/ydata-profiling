import pandas as pd
from pandas_profiling import ProfileReport


if __name__ == "__main__":
    # Suggested by @adamrossnelson
    df = pd.read_stata("http://www.stata-press.com/data/r15/auto2.dta")

    # Length left out due to correlation with weight.
    report = ProfileReport(df, title="1978 Automobile dataset")
    report.to_file("stata_auto_report.html")

    # Pass rejected variables to new profile report.
    # rejected = ProfileReport(df).get_rejected_variables(threshold=0.9)
    # ProfileReport(df[rejected])
