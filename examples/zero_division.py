import pandas as pd

from ydata_profiling import ProfileReport

if __name__ == "__main__":
    import numpy as np

    df = pd.read_csv(
        "c6cb4c3d-e735-4b55-bd5c-b7c78ab152aa.csv", sep=",", encoding="latin"
    )
    # df['empty_col'] = [None]*len(df)

    df.sample(10000)

    df.to_csv("Validation.csv")

    # df.to_csv('teste.csv')

    report = ProfileReport(df, title="Testing the null values")
    report.to_file("report.html")
