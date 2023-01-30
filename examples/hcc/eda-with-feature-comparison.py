"""
    Comparison report example for HCC dataset
"""
import pandas as pd
from sklearn.impute import SimpleImputer

from ydata_profiling import ProfileReport

if __name__ == "__main__":

    # Load the dataset
    df = pd.read_csv("hcc.csv")

    # Produce profile report
    original_report = ProfileReport(df, title="Original Data")
    original_report.to_file("original_report.html")

    # Drop duplicate rows
    df_transformed = df.copy()
    df_transformed = df_transformed.drop_duplicates()

    # Remove O2
    df_transformed = df_transformed.drop(columns="O2")

    # Impute Missing Values
    mean_imputer = SimpleImputer(strategy="mean")
    df_transformed["Ferritin"] = mean_imputer.fit_transform(
        df_transformed["Ferritin"].values.reshape(-1, 1)
    )

    # Produce comparison report
    transformed_report = ProfileReport(df_transformed, title="Transformed Data")
    comparison_report = original_report.compare(transformed_report)
    comparison_report.to_file("original_vs_transformed.html")
