"""Organize the calculation of statistics for each series in this DataFrame."""
from datetime import datetime
from typing import Any, Dict, Optional

import pandas as pd
from tqdm.auto import tqdm
from visions import VisionsTypeset

from pandas_profiling.config import Settings
from pandas_profiling.model.alerts import get_alerts
from pandas_profiling.model.correlations import (
    calculate_correlation,
    get_active_correlations,
)
from pandas_profiling.model.dataframe import check_dataframe, preprocess
from pandas_profiling.model.duplicates import get_duplicates
from pandas_profiling.model.missing import get_missing_active, get_missing_diagram
from pandas_profiling.model.pairwise import get_scatter_plot, get_scatter_tasks
from pandas_profiling.model.sample import get_custom_sample, get_sample
from pandas_profiling.model.summarizer import BaseSummarizer
from pandas_profiling.model.summary import get_series_descriptions
from pandas_profiling.model.table import get_table_stats
from pandas_profiling.utils.progress_bar import progress
from pandas_profiling.version import __version__


def describe(
    config: Settings,
    df: pd.DataFrame,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    sample: Optional[dict] = None,
) -> dict:
    """Calculate the statistics for each series in this DataFrame.

    Args:
        config: report Settings object
        df: DataFrame.
        summarizer: summarizer object
        typeset: visions typeset
        sample: optional, dict with custom sample

    Returns:
        This function returns a dictionary containing:
            - table: overall statistics.
            - variables: descriptions per series.
            - correlations: correlation matrices.
            - missing: missing value diagrams.
            - alerts: direct special attention to these patterns in your data.
            - package: package details.
    """

    if df is None:
        raise ValueError("Can not describe a `lazy` ProfileReport without a DataFrame.")

    check_dataframe(df)
    df = preprocess(config, df)

    number_of_tasks = 5

    with tqdm(
        total=number_of_tasks,
        desc="Summarize dataset",
        disable=not config.progress_bar,
        position=0,
    ) as pbar:
        date_start = datetime.utcnow()

        # Variable-specific
        pbar.total += len(df.columns)
        series_description = get_series_descriptions(
            config, df, summarizer, typeset, pbar
        )

        pbar.set_postfix_str("Get variable types")
        pbar.total += 1
        variables = {
            column: description["type"]
            for column, description in series_description.items()
        }
        supported_columns = [
            column
            for column, type_name in variables.items()
            if type_name != "Unsupported"
        ]
        interval_columns = [
            column for column, type_name in variables.items() if type_name == "Numeric"
        ]
        pbar.update()

        # Get correlations
        correlation_names = get_active_correlations(config)
        pbar.total += len(correlation_names)

        correlations = {
            correlation_name: progress(
                calculate_correlation, pbar, f"Calculate {correlation_name} correlation"
            )(config, df, correlation_name, series_description)
            for correlation_name in correlation_names
        }

        # make sure correlations is not None
        correlations = {
            key: value for key, value in correlations.items() if value is not None
        }

        # Scatter matrix
        pbar.set_postfix_str("Get scatter matrix")
        scatter_tasks = get_scatter_tasks(config, interval_columns)
        pbar.total += len(scatter_tasks)
        scatter_matrix: Dict[Any, Dict[Any, Any]] = {
            x: {y: None} for x, y in scatter_tasks
        }
        for x, y in scatter_tasks:
            scatter_matrix[x][y] = progress(
                get_scatter_plot, pbar, f"scatter {x}, {y}"
            )(config, df, x, y, interval_columns)

        # Table statistics
        table_stats = progress(get_table_stats, pbar, "Get dataframe statistics")(
            config, df, series_description
        )

        # missing diagrams
        missing_map = get_missing_active(config, table_stats)
        pbar.total += len(missing_map)
        missing = {
            name: progress(get_missing_diagram, pbar, f"Missing diagram {name}")(
                config, df, settings
            )
            for name, settings in missing_map.items()
        }
        missing = {name: value for name, value in missing.items() if value is not None}

        # Sample
        pbar.set_postfix_str("Take sample")
        if sample is None:
            samples = get_sample(config, df)
        else:
            samples = get_custom_sample(sample)
        pbar.update()

        # Duplicates
        metrics, duplicates = progress(get_duplicates, pbar, "Detecting duplicates")(
            config, df, supported_columns
        )
        table_stats.update(metrics)

        alerts = progress(get_alerts, pbar, "Get alerts")(
            config, table_stats, series_description, correlations
        )

        pbar.set_postfix_str("Get reproduction details")
        package = {
            "pandas_profiling_version": __version__,
            "pandas_profiling_config": config.json(),
        }
        pbar.update()

        pbar.set_postfix_str("Completed")

        date_end = datetime.utcnow()

    analysis = {
        "title": config.title,
        "date_start": date_start,
        "date_end": date_end,
        "duration": date_end - date_start,
    }

    return {
        # Analysis metadata
        "analysis": analysis,
        # Overall dataset description
        "table": table_stats,
        # Per variable descriptions
        "variables": series_description,
        # Bivariate relations
        "scatter": scatter_matrix,
        # Correlation matrices
        "correlations": correlations,
        # Missing values
        "missing": missing,
        # Alerts
        "alerts": alerts,
        # Package
        "package": package,
        # Sample
        "sample": samples,
        # Duplicates
        "duplicates": duplicates,
    }
