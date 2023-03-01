"""Organize the calculation of statistics for each series in this DataFrame."""
from datetime import datetime
from typing import Any, Dict, Optional

import pandas as pd
from pandas_profiling.config import Settings
from pandas_profiling.model.alerts import get_alerts
from pandas_profiling.model.correlations import (
    calculate_correlation,
    get_active_correlations,
)
from pandas_profiling.model.dataframe import check_dataframe, preprocess
from pandas_profiling.model.description import BaseAnalysis, BaseDescription
from pandas_profiling.model.description_target import TargetDescription, describe_target
from pandas_profiling.model.duplicates import get_duplicates
from pandas_profiling.model.missing import (
    get_missing_active,
    get_missing_description,
    get_missing_diagram,
)
from pandas_profiling.model.pairwise import get_scatter_plot, get_scatter_tasks
from pandas_profiling.model.sample import get_custom_sample, get_sample
from pandas_profiling.model.summarizer import BaseSummarizer
from pandas_profiling.model.summary import get_series_descriptions
from pandas_profiling.model.table import get_table_stats
from pandas_profiling.utils.progress_bar import progress
from pandas_profiling.version import __version__
from tqdm.auto import tqdm
from visions import VisionsTypeset


def describe(
    config: Settings,
    df: pd.DataFrame,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    sample: Optional[dict] = None,
) -> BaseDescription:
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

    check_dataframe(config, df)
    df = preprocess(df)

    number_of_tasks = 5

    with tqdm(
        total=number_of_tasks,
        desc="Summarize dataset",
        disable=not config.progress_bar,
        position=0,
    ) as pbar:
        date_start = datetime.utcnow()

        # target description
        target_description: Optional[TargetDescription]
        if config.target.col_name is not None:
            target_description = describe_target(config.target, df)
        else:
            target_description = None

        # Variable-specific
        pbar.total += len(df.columns)
        series_description = get_series_descriptions(
            config, df, summarizer, typeset, pbar, target_description
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
        if target_description:
            missing["target"] = get_missing_description(config, df, target_description)

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

    # update target description and remove target from variables
    if target_description:
        target_description.description.update(
            series_description[target_description.name]
        )
        del series_description[target_description.name]

    analysis = BaseAnalysis(config.title, date_start, date_end)

    description = BaseDescription(
        analysis=analysis,
        table=table_stats,
        target=target_description,
        variables=series_description,
        scatter=scatter_matrix,
        correlations=correlations,
        missing=missing,
        alerts=alerts,
        package=package,
        sample=samples,
        duplicates=duplicates,
    )
    return description
