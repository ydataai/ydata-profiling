import numpy as np
import pandas as pd
import pytest

import pandas_profiling


@pytest.fixture
def tdf(get_data_file):
    file_name = get_data_file(
        "meteorites.csv",
        "https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD",
    )

    df = pd.read_csv(file_name)

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
    df = df.append(duplicates_to_add, ignore_index=True)
    return df


def test_modular_description_set(tdf):
    profile = tdf.profile_report(
        title="Modular test",
        duplicates=None,
        samples={"head": 0, "tail": 0},
        correlations=None,
        interactions=None,
        missing_diagrams={
            "matrix": False,
            "bar": False,
            "dendrogram": False,
            "heatmap": False,
        },
    )

    html = profile.get_description()
    assert len(html) > 0


def test_modular_absent(tdf):
    profile = tdf.profile_report(
        title="Modular test",
        duplicates={"head": 0},
        samples={"head": 0, "tail": 0},
        interactions=None,
        correlations=None,
        missing_diagrams=None,
    )

    html = profile.to_html()
    assert "Correlations</h1>" not in html
    assert "Duplicate rows</h1>" not in html
    assert "Sample</h1>" not in html
    assert "Missing values</h1>" not in html


def test_modular_present(tdf):
    profile = tdf.profile_report(
        title="Modular test",
        duplicates={"head": 10},
        samples={"head": 10, "tail": 10},
        interactions={"targets": ["mass (g)"], "continuous": True},
        correlations={
            "pearson": {"calculate": True},
            "spearman": {"calculate": True},
            "kendall": {"calculate": True},
            "phi_k": {"calculate": True},
            "cramers": {"calculate": True},
        },
        missing_diagrams={
            "matrix": True,
            "bar": True,
            "dendrogram": True,
            "heatmap": True,
        },
    )

    html = profile.to_html()
    assert "Correlations</h1>" in html
    assert "Duplicate rows</h1>" in html
    assert "Sample</h1>" in html
    assert "Missing values</h1>" in html
