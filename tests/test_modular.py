import pandas as pd
import numpy as np
import pytest

import pandas_profiling


@pytest.fixture
def df():
    df = pd.read_csv(
        "https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD"
    )
    # Note: Pandas does not support dates before 1880, so we ignore these for this analysis
    df["year"] = pd.to_datetime(df["year"], errors="coerce")

    # Example: Constant variable
    df["source"] = "NASA"

    # Example: Boolean variable
    df["boolean"] = np.random.choice([True, False], df.shape[0])

    # Example: Mixed with base types
    df["mixed"] = np.random.choice([1, "A"], df.shape[0])

    # Example: Highly correlated variables
    df["reclat_city"] = df["reclat"] + np.random.normal(scale=5, size=(len(df)))

    # Example: Duplicate observations
    duplicates_to_add = pd.DataFrame(df.iloc[0:10])
    duplicates_to_add["name"] = duplicates_to_add["name"] + " copy"

    df = df.append(duplicates_to_add, ignore_index=True)
    return df


def test_modular_absent(df):
    profile = df.profile_report(
        title="Modular test",
        samples={"head": 0, "tail": 0},
        correlations={
            "pearson": False,
            "spearman": False,
            "kendall": False,
            "phi_k": False,
            "recoded": False,
        },
        missing_diagrams={
            "matrix": False,
            "bar": False,
            "dendrogram": False,
            "heatmap": False,
        },
    )

    assert "Correlations</h1>" not in profile.to_html()
    assert "Sample</h1>" not in profile.to_html()
    assert "Missing values</h1>" not in profile.to_html()


def test_modular_present(df):
    profile = df.profile_report(
        title="Modular test",
        samples={"head": 10, "tail": 10},
        correlations={
            "pearson": True,
            "spearman": True,
            "kendall": True,
            "phi_k": True,
            "recoded": True,
        },
        missing_diagrams={
            "matrix": True,
            "bar": True,
            "dendrogram": True,
            "heatmap": True,
        },
    )

    assert "Correlations</h1>" in profile.to_html()
    assert "Sample</h1>" in profile.to_html()
    assert "Missing values</h1>" in profile.to_html()
