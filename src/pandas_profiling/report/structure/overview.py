from urllib.parse import quote

from pandas_profiling.model.messages import MessageType
from pandas_profiling.report.presentation.core import Container, Table, Warnings


def get_dataset_overview(summary):
    dataset_info = Table(
        [
            {
                "name": "Number of variables",
                "value": summary["table"]["n_var"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Number of observations",
                "value": summary["table"]["n"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Missing cells",
                "value": summary["table"]["n_cells_missing"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Missing cells (%)",
                "value": summary["table"]["p_cells_missing"],
                "fmt": "fmt_percent",
            },
            {
                "name": "Duplicate rows",
                "value": summary["table"]["n_duplicates"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Duplicate rows (%)",
                "value": summary["table"]["p_duplicates"],
                "fmt": "fmt_percent",
            },
            {
                "name": "Total size in memory",
                "value": summary["table"]["memory_size"],
                "fmt": "fmt_bytesize",
            },
            {
                "name": "Average record size in memory",
                "value": summary["table"]["record_size"],
                "fmt": "fmt_bytesize",
            },
        ],
        name="Dataset statistics",
    )

    dataset_types = Table(
        [
            {"name": type_name, "value": count, "fmt": "fmt_numeric"}
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


def get_dataset_reproduction(summary):
    version = summary["package"]["pandas_profiling_version"]
    config = quote(summary["package"]["pandas_profiling_config"])
    date_start = summary["analysis"]["date_start"]
    date_end = summary["analysis"]["date_end"]
    duration = summary["analysis"]["duration"]
    return Table(
        [
            {"name": "Analysis started", "value": date_start, "fmt": "fmt"},
            {"name": "Analysis finished", "value": date_end, "fmt": "fmt"},
            {"name": "Duration", "value": duration, "fmt": "fmt_timespan"},
            {
                "name": "Version",
                "value": f'<a href="https://github.com/pandas-profiling/pandas-profiling">pandas-profiling v{version}</a>',
                "fmt": "raw",
            },
            {
                "name": "Command line",
                "value": "<code>pandas_profiling --config_file config.yaml [YOUR_FILE.csv]</code>",
                "fmt": "raw",
            },
            {
                "name": "Download configuration",
                "value": f'<a download="config.yaml" href="data:text/plain;charset=utf-8,{config}">config.yaml</a>',
                "fmt": "raw",
            },
        ],
        name="Reproduction",
        anchor_id="reproduction",
    )


def get_dataset_warnings(warnings: list) -> Warnings:
    count = len(
        [
            warning
            for warning in warnings
            if warning.message_type != MessageType.REJECTED
        ]
    )
    return Warnings(warnings=warnings, name=f"Warnings ({count})", anchor_id="warnings")
