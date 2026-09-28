"""Missingness pattern detection module for identifying root causes of missing data."""

from dataclasses import dataclass
from typing import Any, List

import numpy as np
import pandas as pd


@dataclass
class MissingnessFinding:
    """Represents a detected missingness pattern between a target and predictor column.

    Attributes:
        target_column: Name of the column with missing values.
        predictor_column: Name of the column whose values correlate with missingness.
        predictor_value: Specific value or interval of the predictor column.
        group_missing_rate: Proportion of missing values in the predictor subgroup.
        overall_missing_rate: Proportion of missing values across the entire dataset.
        effect_size: Difference between group missing rate and overall missing rate.
        support: Number of observations in the predictor subgroup.
    """

    target_column: str
    predictor_column: str
    predictor_value: Any
    group_missing_rate: float
    overall_missing_rate: float
    effect_size: float
    support: int

    def to_sentence(self) -> str:
        """Return a human-readable sentence summarizing the missingness pattern finding.

        Returns:
            A descriptive string summarizing the finding.
        """
        sign = "+" if self.effect_size >= 0 else ""
        return (
            f"Column '{self.target_column}' is missing in {self.group_missing_rate:.1%} "
            f"of rows when '{self.predictor_column}' is '{self.predictor_value}' "
            f"(overall missing rate: {self.overall_missing_rate:.1%}, "
            f"effect size: {sign}{self.effect_size:.2f}, support: {self.support} rows)."
        )


def analyze_missingness_patterns(
    df: pd.DataFrame,
    min_effect: float = 0.2,
    min_support: int = 10,
    max_predictor_cardinality: int = 20,
    numeric_bins: int = 4,
) -> List[MissingnessFinding]:
    """Find columns whose missingness is strongly associated with another column's value.

    Args:
        df: Input pandas DataFrame to analyze.
        min_effect: Minimum absolute effect size (group missing rate minus overall missing rate)
            required to consider a pattern significant.
        min_support: Minimum number of rows required in the subgroup.
        max_predictor_cardinality: Maximum number of distinct categories allowed for a
            predictor column before bucketing (for numeric) or skipping (for non-numeric).
        numeric_bins: Number of quantile bins to discretize high-cardinality numeric predictors.

    Returns:
        List of MissingnessFinding objects, sorted by descending absolute effect size.
    """
    if df is None or len(df) == 0 or len(df.columns) == 0:
        return []

    n_rows = len(df)

    # Identify candidate target columns (columns with non-trivial missingness)
    target_columns = sorted(
        [col for col in df.columns if 0 < int(df[col].isna().sum()) < n_rows]
    )

    if not target_columns:
        return []

    # Preprocess candidate predictor columns to ensure deterministic, efficient grouping
    processed_predictors = {}
    for col in sorted(df.columns):
        series = df[col]
        n_unique = int(series.nunique(dropna=True))

        # Skip constant columns or completely missing columns
        if n_unique <= 1:
            continue

        is_numeric = pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series)

        if is_numeric:
            if n_unique > max_predictor_cardinality:
                try:
                    # Quantile bucketing for numeric predictors with high cardinality
                    binned = pd.qcut(series, q=numeric_bins, duplicates="drop")
                    processed_predictors[col] = binned
                except Exception:
                    continue
            else:
                processed_predictors[col] = series
        else:
            # Skip high-cardinality non-numeric columns (e.g. IDs, free text, UUIDs)
            if n_unique > max_predictor_cardinality:
                continue
            if n_rows > 10 and (n_unique / n_rows) > 0.5:
                continue
            processed_predictors[col] = series

    findings: List[MissingnessFinding] = []

    for target_col in target_columns:
        overall_missing_mask = df[target_col].isna()
        overall_missing_count = int(overall_missing_mask.sum())
        overall_missing_rate = float(overall_missing_count / n_rows)

        for pred_col, pred_series in processed_predictors.items():
            if pred_col == target_col:
                continue

            unique_values = pred_series.dropna().unique()
            # Sort unique values deterministically
            try:
                sorted_values = sorted(unique_values)
            except TypeError:
                sorted_values = sorted(unique_values, key=lambda x: str(x))

            for val in sorted_values:
                group_mask = pred_series == val
                support = int(group_mask.sum())

                if support < min_support:
                    continue

                group_missing_count = int((overall_missing_mask & group_mask).sum())
                group_missing_rate = float(group_missing_count / support)
                effect_size = float(group_missing_rate - overall_missing_rate)

                if abs(effect_size) >= min_effect:
                    finding_val = str(val) if isinstance(val, pd.Interval) else val
                    findings.append(
                        MissingnessFinding(
                            target_column=target_col,
                            predictor_column=pred_col,
                            predictor_value=finding_val,
                            group_missing_rate=round(group_missing_rate, 4),
                            overall_missing_rate=round(overall_missing_rate, 4),
                            effect_size=round(effect_size, 4),
                            support=support,
                        )
                    )

    # Sort deterministically by descending absolute effect size, then descending support, then column names
    findings.sort(
        key=lambda f: (
            -abs(f.effect_size),
            -f.support,
            f.target_column,
            f.predictor_column,
            str(f.predictor_value),
        )
    )

    return findings


def findings_to_dataframe(findings: List[MissingnessFinding]) -> pd.DataFrame:
    """Convert a list of MissingnessFinding instances into a pandas DataFrame.

    Args:
        findings: List of MissingnessFinding objects.

    Returns:
        DataFrame containing all finding fields as columns.
    """
    if not findings:
        return pd.DataFrame(
            columns=[
                "target_column",
                "predictor_column",
                "predictor_value",
                "group_missing_rate",
                "overall_missing_rate",
                "effect_size",
                "support",
            ]
        )

    records = [
        {
            "target_column": f.target_column,
            "predictor_column": f.predictor_column,
            "predictor_value": f.predictor_value,
            "group_missing_rate": f.group_missing_rate,
            "overall_missing_rate": f.overall_missing_rate,
            "effect_size": f.effect_size,
            "support": f.support,
        }
        for f in findings
    ]
    return pd.DataFrame.from_records(records)
