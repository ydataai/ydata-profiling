"""Unit tests for outlier detection module."""

import pickle
import numpy as np
import pandas as pd
import pytest

from data_profiling.model.smart_insights.outliers import (
    ColumnOutlierReport,
    detect_outliers,
    outliers_to_dataframe,
)


def test_planted_outliers_iqr_and_zscore() -> None:
    """Test planting known outliers at known indices and verifying exact detection."""
    # 100 rows with baseline values in [10.0, 12.0]
    data = [10.0, 11.0, 12.0, 10.5, 11.5] * 20
    # Plant outliers at specific indices
    data[5] = 1000.0   # Extreme high outlier
    data[42] = -500.0  # Extreme low outlier

    df = pd.DataFrame({"val": data})

    # 1. Test IQR method
    iqr_results = detect_outliers(df, method="iqr")
    assert "val" in iqr_results
    rep_iqr = iqr_results["val"]
    assert rep_iqr.method == "iqr"
    assert rep_iqr.outlier_indices == [5, 42]
    assert rep_iqr.n_outliers == 2
    assert rep_iqr.pct_outliers == 0.02
    assert rep_iqr.lower_bound < 10.0
    assert rep_iqr.upper_bound > 12.0

    # Test sentence
    sentence_iqr = rep_iqr.to_sentence()
    assert "val" in sentence_iqr
    assert "2 outliers" in sentence_iqr
    assert "IQR" in sentence_iqr

    # 2. Test Z-score method
    z_results = detect_outliers(df, method="zscore", z_thresh=3.0)
    assert "val" in z_results
    rep_z = z_results["val"]
    assert rep_z.method == "zscore"
    assert rep_z.outlier_indices == [5, 42]
    assert rep_z.n_outliers == 2
    assert rep_z.pct_outliers == 0.02


def test_clean_data_negative_case() -> None:
    """Test that evenly distributed data without outliers returns 0 outliers."""
    # Linear sequence without outliers
    data = list(range(10, 50))
    df = pd.DataFrame({"clean": data})

    results = detect_outliers(df, method="iqr")
    assert "clean" in results
    rep = results["clean"]
    assert rep.n_outliers == 0
    assert rep.outlier_indices == []
    assert rep.pct_outliers == 0.0


def test_outliers_to_dataframe() -> None:
    """Test export of outlier detection reports to a pandas DataFrame."""
    rep = ColumnOutlierReport(
        column="col_x",
        method="iqr",
        lower_bound=-5.0,
        upper_bound=25.0,
        n_outliers=3,
        pct_outliers=0.03,
        outlier_indices=[1, 4, 99],
    )
    df_out = outliers_to_dataframe({"col_x": rep})
    assert isinstance(df_out, pd.DataFrame)
    assert len(df_out) == 1
    assert df_out.iloc[0]["column"] == "col_x"
    assert df_out.iloc[0]["method"] == "iqr"
    assert df_out.iloc[0]["n_outliers"] == 3
    assert df_out.iloc[0]["outlier_indices"] == [1, 4, 99]

    # Test empty dictionary export
    df_empty = outliers_to_dataframe({})
    assert isinstance(df_empty, pd.DataFrame)
    assert len(df_empty) == 0
    assert "column" in df_empty.columns
    assert "n_outliers" in df_empty.columns


def test_invalid_method_raises_value_error() -> None:
    """Test that unsupported method raises ValueError."""
    df = pd.DataFrame({"a": [1, 2, 3]})
    with pytest.raises(ValueError, match="Unsupported outlier detection method"):
        detect_outliers(df, method="invalid_method")


def test_outlier_deterministic_behavior() -> None:
    """Test that detect_outliers produces byte-identical output across runs."""
    np.random.seed(42)
    df = pd.DataFrame({
        "num_a": np.random.normal(loc=50, scale=5, size=100),
        "num_b": np.random.exponential(scale=10, size=100),
    })

    run1 = detect_outliers(df, method="iqr")
    run2 = detect_outliers(df, method="iqr")

    assert pickle.dumps(run1) == pickle.dumps(run2), "Output must be byte-identical across runs!"
