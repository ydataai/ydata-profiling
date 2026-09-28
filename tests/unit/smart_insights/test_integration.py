"""Integration tests verifying end-to-end Smart Insights and Alert pipeline integration."""

import numpy as np
import pandas as pd
import pytest

from data_profiling import ProfileReport
from data_profiling.config import Settings
from data_profiling.model.alerts import AlertType, MissingnessPatternAlert, OutlierAlert


def test_profile_report_smart_insights_integration() -> None:
    """Test that ProfileReport generates alerts and Smart Insights section in HTML."""
    np.random.seed(42)
    n = 100
    # Plant missingness: col_a missing when col_b == 'x'
    col_b = ["x"] * 50 + ["y"] * 50
    col_a = [np.nan] * 50 + [5.0] * 50
    # Plant outlier in col_c
    col_c = [10.0, 11.0, 12.0, 10.5, 11.5] * 20
    col_c[7] = 999.0

    df = pd.DataFrame({"col_a": col_a, "col_b": col_b, "col_c": col_c})

    report = ProfileReport(df, progress_bar=False)
    description = report.description_set

    # Verify alerts list contains our custom alert types
    alert_types = [a.alert_type for a in description.alerts]
    assert AlertType.MISSINGNESS_PATTERN in alert_types
    assert AlertType.OUTLIER in alert_types

    # Verify smart_insights data is attached to description
    assert description.smart_insights is not None
    assert "missingness" in description.smart_insights
    assert "outliers" in description.smart_insights

    findings = description.smart_insights["missingness"]
    assert len(findings) > 0
    assert any(f.target_column == "col_a" and f.predictor_column == "col_b" for f in findings)

    outliers = description.smart_insights["outliers"]
    assert "col_c" in outliers
    assert outliers["col_c"].n_outliers == 1
    assert 7 in outliers["col_c"].outlier_indices

    # Render HTML and verify smart insights section is present
    html = report.to_html()
    assert "Smart Insights" in html
    assert "Missingness Root-Cause Patterns" in html
    assert "Outlier Analysis" in html
    assert "col_a" in html
    assert "col_c" in html


def test_custom_config_thresholds() -> None:
    """Test that custom config thresholds are applied to analysis."""
    np.random.seed(42)
    # Plant a subtle pattern: effect size = 0.25
    col_b = ["x"] * 40 + ["y"] * 60
    # col_a missing 50% when x (20/40), missing 25% when y (15/60)
    col_a = [np.nan] * 20 + [1.0] * 20 + [np.nan] * 15 + [1.0] * 45
    df = pd.DataFrame({"col_a": col_a, "col_b": col_b})

    # With high min_effect (0.5), pattern should NOT be flagged
    strict_config = Settings()
    strict_config.smart_insights.min_effect = 0.5
    report_strict = ProfileReport(df, config=strict_config, progress_bar=False)
    findings_strict = report_strict.description_set.smart_insights["missingness"]
    assert len(findings_strict) == 0

    # With lower min_effect (0.1), pattern SHOULD be flagged
    lenient_config = Settings()
    lenient_config.smart_insights.min_effect = 0.1
    report_lenient = ProfileReport(df, config=lenient_config, progress_bar=False)
    findings_lenient = report_lenient.description_set.smart_insights["missingness"]
    assert len(findings_lenient) > 0

