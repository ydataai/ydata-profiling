from typing import Optional
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


def get_dataset_schema(metadata) -> Optional[Table]:
    if len(metadata) > 0 or any(len(value) > 0 for value in metadata.values()):
        about_dataset = []
        for key in ["description", "creator", "author", "url"]:
            if key in metadata and len(metadata[key]) > 0:
                about_dataset.append(
                    {"name": key.capitalize(), "value": metadata[key], "fmt": "fmt"}
                )

        if "copyright_holder" in metadata and len(metadata["copyright_holder"]) > 0:
            if "copyright_year" not in metadata:
                about_dataset.append(
                    {
                        "name": "Copyright",
                        "value": f"(c) {metadata['copyright_holder']}",
                        "fmt": "fmt",
                    }
                )
            else:
                about_dataset.append(
                    {
                        "name": "Copyright",
                        "value": f"(c) {metadata['copyright_holder']} {metadata['copyright_year']}",
                        "fmt": "fmt",
                    }
                )

        if len(about_dataset) > 0:
            return Table(about_dataset, name="Dataset", anchor_id="metadata_dataset")


def get_dataset_reproduction(summary: dict, metadata: dict):
    version = summary["package"]["pandas_profiling_version"]
    config = quote(summary["package"]["pandas_profiling_config"])
    date_start = summary["analysis"]["date_start"]
    date_end = summary["analysis"]["date_end"]
    duration = summary["analysis"]["duration"]

    reproduction_table = Table(
        [
            {"name": "Analysis started", "value": date_start, "fmt": "fmt"},
            {"name": "Analysis finished", "value": date_end, "fmt": "fmt"},
            {"name": "Duration", "value": duration, "fmt": "fmt_timespan"},
            {
                "name": "Software version",
                "value": f'<a href="https://github.com/pandas-profiling/pandas-profiling">pandas-profiling v{version}</a>',
                "fmt": "raw",
            },
            {
                "name": "Download configuration",
                "value": f'<a download="config.yaml" href="data:text/plain;charset=utf-8,{config}">config.yaml</a>',
                "fmt": "raw",
            },
        ],
        name="Reproduction",
        anchor_id="metadata_reproduction",
    )

    dataset_table = get_dataset_schema(metadata)

    items = []
    if dataset_table:
        items.append(dataset_table)
    items.append(reproduction_table)

    return Container(
        items, name="Metadata", anchor_id="metadata", sequence_type="grid",
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
