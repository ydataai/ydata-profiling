"""Unit tests for missingness root-cause pattern detection."""

import pickle
import numpy as np
import pandas as pd
import pytest

from data_profiling.model.smart_insights.missingness import (
    MissingnessFinding,
    analyze_missingness_patterns,
    findings_to_dataframe,
)


def test_planted_missingness_pattern() -> None:
    """Test detection of a planted missingness pattern with exact numbers verified."""
    np.random.seed(42)
    # 100 rows: predictor 'x' 50 times, 'y' 50 times
    # Target is missing only when predictor == 'x'
    predictor = ["x"] * 50 + ["y"] * 50
    target = [np.nan] * 50 + [1.0] * 50

    df = pd.DataFrame({"target": target, "predictor": predictor})

    findings = analyze_missingness_patterns(df, min_effect=0.2, min_support=10)

    # Both x (elevated missingness) and y (suppressed missingness) exceed min_effect=0.2
    assert len(findings) == 2

    # First finding must be predictor == 'x' with highest effect size
    f_x = findings[0]
    assert f_x.target_column == "target"
    assert f_x.predictor_column == "predictor"
    assert f_x.predictor_value == "x"
    assert f_x.group_missing_rate == 1.0
    assert f_x.overall_missing_rate == 0.5
    assert f_x.effect_size == 0.5
    assert f_x.support == 50

    # Second finding must be predictor == 'y'
    f_y = findings[1]
    assert f_y.target_column == "target"
    assert f_y.predictor_column == "predictor"
    assert f_y.predictor_value == "y"
    assert f_y.group_missing_rate == 0.0
    assert f_y.overall_missing_rate == 0.5
    assert f_y.effect_size == -0.5
    assert f_y.support == 50

    # Test sentence formatting
    sentence = f_x.to_sentence()
    assert "target" in sentence
    assert "predictor" in sentence
    assert "100.0%" in sentence
    assert "+0.50" in sentence
    assert "50" in sentence


def test_independent_random_columns_negative_case() -> None:
    """Test that two independent random columns produce NO missingness findings."""
    np.random.seed(123)
    n = 1000
    predictor = np.random.choice(["cat_a", "cat_b", "cat_c", "cat_d"], size=n)
    # Target missingness independent of predictor (missing ~25%)
    target = np.random.choice([1.0, np.nan], size=n, p=[0.75, 0.25])

    df = pd.DataFrame({"target": target, "predictor": predictor})

    findings = analyze_missingness_patterns(df, min_effect=0.15, min_support=20)
    assert len(findings) == 0, f"Expected 0 findings for independent columns, got: {findings}"


def test_numeric_predictor_bucketing() -> None:
    """Test quantile bucketing when numeric predictor exceeds max_predictor_cardinality."""
    np.random.seed(99)
    n = 100
    num_pred = np.linspace(0.0, 100.0, n)
    # Missing when num_pred > 75 (top quartile)
    target = np.where(num_pred > 75.0, np.nan, 10.0)

    df = pd.DataFrame({"target": target, "num_pred": num_pred})

    findings = analyze_missingness_patterns(
        df,
        min_effect=0.2,
        min_support=10,
        max_predictor_cardinality=10,
        numeric_bins=4,
    )
    assert len(findings) > 0
    # Top bucket should have elevated missingness
    top_finding = findings[0]
    assert top_finding.target_column == "target"
    assert top_finding.predictor_column == "num_pred"
    assert top_finding.effect_size > 0.4


def test_skip_high_cardinality_non_numeric_columns() -> None:
    """Test that unique ID / free-text non-numeric columns are skipped as predictors."""
    np.random.seed(7)
    n = 50
    user_ids = [f"usr_{i:04d}" for i in range(n)]
    target = [np.nan if i < 15 else 1.0 for i in range(n)]

    df = pd.DataFrame({"target": target, "user_id": user_ids})

    findings = analyze_missingness_patterns(df, min_effect=0.1, min_support=1, max_predictor_cardinality=10)
    # user_id should be skipped entirely because cardinality exceeds max_predictor_cardinality
    assert len(findings) == 0


def test_findings_to_dataframe() -> None:
    """Test export of MissingnessFinding objects to a pandas DataFrame."""
    f = MissingnessFinding(
        target_column="col_a",
        predictor_column="col_b",
        predictor_value="val_1",
        group_missing_rate=0.8,
        overall_missing_rate=0.4,
        effect_size=0.4,
        support=25,
    )
    df_out = findings_to_dataframe([f])
    assert isinstance(df_out, pd.DataFrame)
    assert len(df_out) == 1
    assert df_out.iloc[0]["target_column"] == "col_a"
    assert df_out.iloc[0]["predictor_column"] == "col_b"
    assert df_out.iloc[0]["effect_size"] == 0.4
    assert df_out.iloc[0]["support"] == 25

    # Test empty findings export
    df_empty = findings_to_dataframe([])
    assert isinstance(df_empty, pd.DataFrame)
    assert len(df_empty) == 0
    assert "target_column" in df_empty.columns
    assert "effect_size" in df_empty.columns


def test_missingness_deterministic_behavior() -> None:
    """Test that analyze_missingness_patterns produces byte-identical output across runs."""
    np.random.seed(42)
    df = pd.DataFrame({
        "A": [1.0, np.nan, np.nan, 4.0, 5.0] * 20,
        "B": ["alpha", "beta", "alpha", "gamma", "beta"] * 20,
        "C": [10, 20, 30, 40, 50] * 20,
    })

    run1 = analyze_missingness_patterns(df, min_effect=0.1, min_support=5)
    run2 = analyze_missingness_patterns(df, min_effect=0.1, min_support=5)

    assert pickle.dumps(run1) == pickle.dumps(run2), "Output must be byte-identical across runs!"
