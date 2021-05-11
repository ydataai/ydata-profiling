from typing import List
from urllib.parse import quote

from pandas_profiling.config import Settings
from pandas_profiling.model.alerts import AlertType
from pandas_profiling.report.formatters import (
    fmt,
    fmt_bytesize,
    fmt_number,
    fmt_numeric,
    fmt_percent,
    fmt_timespan,
)
from pandas_profiling.report.presentation.core import Alerts, Container, Table
from pandas_profiling.report.presentation.core.renderable import Renderable


def get_dataset_overview(config: Settings, summary: dict) -> Renderable:
    table_metrics = [
        {
            "name": "Number of variables",
            "value": fmt_number(summary["table"]["n_var"]),
        },
        {
            "name": "Number of observations",
            "value": fmt_number(summary["table"]["n"]),
        },
        {
            "name": "Missing cells",
            "value": fmt_number(summary["table"]["n_cells_missing"]),
        },
        {
            "name": "Missing cells (%)",
            "value": fmt_percent(summary["table"]["p_cells_missing"]),
        },
    ]
    if "n_duplicates" in summary["table"]:
        table_metrics.extend(
            [
                {
                    "name": "Duplicate rows",
                    "value": fmt_number(summary["table"]["n_duplicates"]),
                },
                {
                    "name": "Duplicate rows (%)",
                    "value": fmt_percent(summary["table"]["p_duplicates"]),
                },
            ]
        )

    table_metrics.extend(
        [
            {
                "name": "Total size in memory",
                "value": fmt_bytesize(summary["table"]["memory_size"]),
            },
            {
                "name": "Average record size in memory",
                "value": fmt_bytesize(summary["table"]["record_size"]),
            },
        ]
    )

    dataset_info = Table(
        table_metrics,
        name="Dataset statistics",
    )

    dataset_types = Table(
        [
            {
                "name": str(type_name),
                "value": fmt_numeric(count, precision=config.report.precision),
            }
            for type_name, count in summary["table"]["types"].items()
        ],
        name="Variable types",
    )

    return Container(
        [dataset_info, dataset_types],
        anchor_id="dataset_overview",
        name="Overview",
        sequence_type="grid",
    )


def get_dataset_schema(metadata: dict) -> Container:
    about_dataset = []
    for key in ["description", "creator", "author"]:
        if key in metadata and len(metadata[key]) > 0:
            about_dataset.append(
                {"name": key.capitalize(), "value": fmt(metadata[key])}
            )

    if "url" in metadata:
        about_dataset.append(
            {
                "name": "URL",
                "value": f'<a href="{metadata["url"]}">{metadata["url"]}</a>',
            }
        )

    if "copyright_holder" in metadata and len(metadata["copyright_holder"]) > 0:
        if "copyright_year" not in metadata:
            about_dataset.append(
                {
                    "name": "Copyright",
                    "value": fmt(f"(c) {metadata['copyright_holder']}"),
                }
            )
        else:
            about_dataset.append(
                {
                    "name": "Copyright",
                    "value": fmt(
                        f"(c) {metadata['copyright_holder']} {metadata['copyright_year']}"
                    ),
                }
            )

    return Container(
        [Table(about_dataset, name="Dataset", anchor_id="metadata_dataset")],
        name="Dataset",
        anchor_id="dataset",
        sequence_type="grid",
    )


def get_dataset_reproduction(summary: dict) -> Renderable:
    version = summary["package"]["pandas_profiling_version"]
    config = quote(summary["package"]["pandas_profiling_config"])
    date_start = summary["analysis"]["date_start"]
    date_end = summary["analysis"]["date_end"]
    duration = summary["analysis"]["duration"]

    reproduction_table = Table(
        [
            {"name": "Analysis started", "value": fmt(date_start)},
            {"name": "Analysis finished", "value": fmt(date_end)},
            {"name": "Duration", "value": fmt_timespan(duration)},
            {
                "name": "Software version",
                "value": f'<a href="https://github.com/pandas-profiling/pandas-profiling">pandas-profiling v{version}</a>',
            },
            {
                "name": "Download configuration",
                "value": f'<a download="config.json" href="data:text/plain;charset=utf-8,{config}">config.json</a>',
            },
        ],
        name="Reproduction",
        anchor_id="overview_reproduction",
    )

    return Container(
        [reproduction_table],
        name="Reproduction",
        anchor_id="reproduction",
        sequence_type="grid",
    )


def get_dataset_column_definitions(definitions: dict) -> Container:
    """Generate an overview section for the variable description

    Args:
        definitions: the variable descriptions.

    Returns:
        A container object
    """

    variable_descriptions = [
        Table(
            [
                {"name": column, "value": fmt(value)}
                for column, value in definitions.items()
            ],
            name="Variable descriptions",
            anchor_id="variable_definition_table",
        )
    ]

    return Container(
        variable_descriptions,
        name="Variables",
        anchor_id="variable_descriptions",
        sequence_type="grid",
    )


def get_dataset_alerts(alerts: list) -> Alerts:
    count = len([alert for alert in alerts if alert.alert_type != AlertType.REJECTED])
    return Alerts(alerts=alerts, name=f"Alerts ({count})", anchor_id="alerts")


def get_dataset_items(config: Settings, summary: dict, alerts: list) -> list:
    """Returns the dataset overview (at the top of the report)

    Args:
        summary: the calculated summary
        alerts: the alerts

    Returns:
        A list with components for the dataset overview (overview, reproduction, alerts)
    """

    items: List[Renderable] = [get_dataset_overview(config, summary)]

    metadata = {key: config.dataset.dict()[key] for key in config.dataset.dict().keys()}

    if len(metadata) > 0 and any(len(value) > 0 for value in metadata.values()):
        items.append(get_dataset_schema(metadata))

    column_details = {
        key: config.variables.descriptions[key]
        for key in config.variables.descriptions.keys()
    }

    if len(column_details) > 0:
        items.append(get_dataset_column_definitions(column_details))

    if alerts:
        items.append(get_dataset_alerts(alerts))

    items.append(get_dataset_reproduction(summary))

    return items
