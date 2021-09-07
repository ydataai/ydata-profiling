from typing import Any, Dict

from pandas_profiling.config import Settings
from pandas_profiling.report.formatters import fmt, fmt_bytesize, fmt_percent
from pandas_profiling.report.presentation.core import (
    Container,
    Image,
    Table,
    VariableInfo,
)
from pandas_profiling.visualisation.plot import histogram, mini_histogram


def render_date(config: Settings, summary: Dict[str, Any]) -> Dict[str, Any]:
    varid = summary["varid"]
    template_variables = {}

    image_format = config.plot.image_format

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Date",
        summary["alerts"],
        summary["description"],
    )

    table1 = Table(
        [
            {
                "name": "Distinct",
                "value": fmt(summary["n_distinct"]),
                "alert": False,
            },
            {
                "name": "Distinct (%)",
                "value": fmt_percent(summary["p_distinct"]),
                "alert": False,
            },
            {
                "name": "Missing",
                "value": fmt(summary["n_missing"]),
                "alert": False,
            },
            {
                "name": "Missing (%)",
                "value": fmt_percent(summary["p_missing"]),
                "alert": False,
            },
            {
                "name": "Memory size",
                "value": fmt_bytesize(summary["memory_size"]),
                "alert": False,
            },
        ]
    )

    table2 = Table(
        [
            {"name": "Minimum", "value": fmt(summary["min"]), "alert": False},
            {"name": "Maximum", "value": fmt(summary["max"]), "alert": False},
        ]
    )

    img = ""
    if summary["histogram"] is not None:
        img = mini_histogram(
            config, summary["histogram"][0], summary["histogram"][1], date=True
        )

    mini_histo = Image(
        img,
        image_format=image_format,
        alt="Mini histogram",
    )

    template_variables["top"] = Container(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    img = ""
    if summary["histogram"] is not None:
        img = histogram(
            config, summary["histogram"][0], summary["histogram"][1], date=True
        )
        # (bins={len(summary['histogram'][1]) - 1})

    # Bottom
    bottom = Container(
        [
            Image(
                img,
                image_format=image_format,
                alt="Histogram",
                caption=f"<strong>Histogram with fixed size bins</strong>",
                name="Histogram",
                anchor_id=f"{varid}histogram",
            )
        ],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    template_variables["bottom"] = bottom

    return template_variables
