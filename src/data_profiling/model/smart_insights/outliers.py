"""Outlier detection module for numeric columns using IQR and Z-score methods."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


@dataclass
class ColumnOutlierReport:
    """Summary of outlier analysis for a single numeric column.

    Attributes:
        column: Column name analyzed.
        method: Method used for detection ('iqr' or 'zscore').
        lower_bound: Lower numerical boundary for regular values.
        upper_bound: Upper numerical boundary for regular values.
        n_outliers: Count of observations falling outside the boundaries.
        pct_outliers: Proportion of total rows identified as outliers.
        outlier_indices: List of row indices corresponding to outliers.
    """

    column: str
    method: str
    lower_bound: float
    upper_bound: float
    n_outliers: int
    pct_outliers: float
    outlier_indices: List[Any]

    def to_sentence(self) -> str:
        """Return a human-readable sentence summarizing the outlier detection findings.

        Returns:
            A descriptive string summarizing outlier counts and bounds.
        """
        return (
            f"Column '{self.column}' has {self.n_outliers} outliers ({self.pct_outliers:.1%}) "
            f"detected using {self.method.upper()} outside bounds [{self.lower_bound:.2f}, {self.upper_bound:.2f}]."
        )


def detect_outliers(
    df: pd.DataFrame,
    method: str = "iqr",
    z_thresh: float = 3.0,
    columns: Optional[List[str]] = None,
) -> Dict[str, ColumnOutlierReport]:
    """Detect outliers for numeric columns in a DataFrame using IQR or Z-score method.

    Args:
        df: Input pandas DataFrame to analyze.
        method: Detection technique to apply; either 'iqr' (1.5 * IQR) or 'zscore'.
        z_thresh: Z-score cutoff multiplier (applied when method is 'zscore').
        columns: Optional list of specific column names to check. Defaults to all numeric columns.

    Returns:
        Dictionary mapping column names to ColumnOutlierReport instances.

    Raises:
        ValueError: If method is not one of 'iqr' or 'zscore'.
    """
    normalized_method = method.strip().lower()
    if normalized_method not in {"iqr", "zscore"}:
        raise ValueError(
            f"Unsupported outlier detection method '{method}'. Choose 'iqr' or 'zscore'."
        )

    if df is None or len(df) == 0:
        return {}

    # Determine numeric candidate columns
    if columns is None:
        target_columns = [
            col
            for col in df.columns
            if pd.api.types.is_numeric_dtype(df[col])
            and not pd.api.types.is_bool_dtype(df[col])
        ]
    else:
        target_columns = [
            col
            for col in columns
            if col in df.columns
            and pd.api.types.is_numeric_dtype(df[col])
            and not pd.api.types.is_bool_dtype(df[col])
        ]

    # Sort target columns deterministically
    target_columns = sorted(target_columns)

    reports: Dict[str, ColumnOutlierReport] = {}
    total_rows = len(df)

    for col in target_columns:
        series = df[col].dropna()
        if len(series) == 0:
            reports[col] = ColumnOutlierReport(
                column=col,
                method=normalized_method,
                lower_bound=0.0,
                upper_bound=0.0,
                n_outliers=0,
                pct_outliers=0.0,
                outlier_indices=[],
            )
            continue

        if normalized_method == "iqr":
            q25 = float(series.quantile(0.25))
            q75 = float(series.quantile(0.75))
            iqr = q75 - q25
            lower_bound = float(q25 - 1.5 * iqr)
            upper_bound = float(q75 + 1.5 * iqr)
        else:  # zscore
            mean = float(series.mean())
            std = float(series.std(ddof=0))
            if std == 0.0:
                lower_bound = mean
                upper_bound = mean
            else:
                lower_bound = float(mean - z_thresh * std)
                upper_bound = float(mean + z_thresh * std)

        outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_indices = df.index[outlier_mask].tolist()
        n_outliers = len(outlier_indices)
        pct_outliers = float(n_outliers / total_rows) if total_rows > 0 else 0.0

        reports[col] = ColumnOutlierReport(
            column=col,
            method=normalized_method,
            lower_bound=round(lower_bound, 4),
            upper_bound=round(upper_bound, 4),
            n_outliers=n_outliers,
            pct_outliers=round(pct_outliers, 4),
            outlier_indices=outlier_indices,
        )

    return reports


def outliers_to_dataframe(results: Dict[str, ColumnOutlierReport]) -> pd.DataFrame:
    """Convert outlier detection results dictionary into a pandas DataFrame.

    Args:
        results: Dictionary mapping column names to ColumnOutlierReport objects.

    Returns:
        DataFrame containing outlier metrics across analyzed columns.
    """
    if not results:
        return pd.DataFrame(
            columns=[
                "column",
                "method",
                "lower_bound",
                "upper_bound",
                "n_outliers",
                "pct_outliers",
                "outlier_indices",
            ]
        )

    records = [
        {
            "column": r.column,
            "method": r.method,
            "lower_bound": r.lower_bound,
            "upper_bound": r.upper_bound,
            "n_outliers": r.n_outliers,
            "pct_outliers": r.pct_outliers,
            "outlier_indices": r.outlier_indices,
        }
        for r in results.values()
    ]
    return pd.DataFrame.from_records(records)
